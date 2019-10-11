
import requests
import json
import sys
import argparse
import time


class NeoGeo:
    def __init__(self):

        # Put your IPStack token here, or pass --token
        self.token = "PUT YOUR IPSTACK TOKEN HERE NAO"

        self.parser = argparse.ArgumentParser(description="Geolocate a single ip, or a list of them. "
                                                          "Requires an ipstack API key")

        self.parser.add_argument("-ip",
                                 "--ip",
                                 type=str,
                                 help="Input a  single IP address to check")

        self.parser.add_argument("--ips",
                                 type=str,
                                 help="Point to a file, new-line separated, containing multiple IP addresses.")

        self.parser.add_argument("--token",
                                 type=str,
                                 help="Your IP Stack API token")

        self.parser.add_argument("-f",
                                 "--format",
                                 type=str,
                                 help="The file output format. Options: json, csv, tsv")

        self.parser.add_argument("-hc",
                                 "--hide",
                                 action="store_true",
                                 help="Hide the columns and just output the results.")

        self.parser.add_argument("--full",
                                 action="store_true",
                                 help="Decide whether or not to output a bunch of redundant information.")

        self.args = self.parser.parse_args()
        # Valid output format options.

        # I could combine these too, but I'm too lazy to recode stuff. Get over yourself. Oh wait, I am myself.
        self.format_list = ["json", "csv", "tsv"]
        self.format_dict = {
            ",": "csv",
            "\t": "tsv"
        }

        # There's a bit of redundant information otherwise.
        self.full_output = False
        self.output_format = "tsv"
        self.input_file = None
        self.file_handle = None
        self.column_printed = False

        # In case you just want results with no columns.
        self.hide_column = False

        self.short_list = []
        self.output_list = []
        self.is_column = True

        # This is for CSV and TSV purposes.
        # When not showing full info.
        self.short_columns = [
            "ip",
            "location",
            "city",
            "region_name",
            "zip",
            "country_name",
            "continent_name",
            "latitude",
            "longitude",
        ]
        self.output_column_names = [
            "ip",
            "type",
            "continent_code",
            "continent_name",
            "country_code",
            "country_name",
            "region_code",
            "region_name",
            "city",
            "zip",
            "latitude",
            "longitude",
            "location"
        ]
        # Now let's see what we can do...
        self.determine_actions()

    # You did a bad thing. The program is now mad.
    def rage_quit(self):
        self.parser.print_help()
        sys.exit(0)

    def determine_actions(self):
        # If the token string is set, let's use that.
        if self.args.token:
            self.token = self.args.token.lower()

        # If you don't want to see columns, use -hc, --hide.
        if self.args.hide:
            self.hide_column = True

        # Do you want a full output? This basically makes it look terrible until I can somehow fix it. Use --full.
        if self.args.full:
            # --full and --format json are redundant.
            self.full_output = False if self.args.format == "json" else True

        # If the format string is set, let's take a look and see if it matches a valid format from self.format_list.
        if self.args.format:
            found = False
            for f in self.format_list:
                # Cool, we found a valid format. Let's do some stuff...
                if f.lower() == self.args.format:
                    self.output_format = self.args.format
                    found = True
                    # We don't need to keep this loop going, we found what we wanted.
                    break
            if not found:
                print("You chose an invalid output format. Defaulting to tab-separated values (TSV).")

        # This gets confirmed if the IP address is added as a string.
        if self.args.ip and self.token:
            self.geolocate_ip(self.args.ip)

        # Do we have a list of IPs instead? Let's use that.
        elif self.args.ips and self.token:
            self.input_file = self.args.ips
            self.geolocate_ips_from_list()

        else:
            self.rage_quit()

    def make_request(self, ip):
        return requests.get(f"http://api.ipstack.com/{ip}?access_key={self.token}")

    def check_content(self, request):
        content = str(request.content.decode("utf8").replace("'", '"'))
        if content:
            json_contents = json.loads(content)
            for column in self.output_column_names:
                self.output_list.append(json_contents.get(column)['country_flag_emoji']
                                        if column == "location"
                                        else json_contents.get(column))

            if not self.full_output:
                for column in self.short_columns:
                    self.short_list.append(json_contents.get(column)['country_flag_emoji']
                                           if column == "location"
                                           else json_contents.get(column))

            # Now let's print the content. JSON is already done, so we can just directly return the content string.
            # Otherwise, we need to get the rows.
            if self.file_handle:
                self.write_print(content if self.output_format == "json" else self.get_rows())
            else:
                print(content if self.output_format == "json" else self.get_rows())

    def geolocate_ip(self, ip):
        try:
            r = self.make_request(ip)
            if r.status_code == 200:
                # If this is a tsv or csv output, the first thing we do is output the columns.
                if not self.hide_column:
                    print(self.get_columns())
                self.is_column = False
                self.check_content(r)
        # Don't really care right now.
        except ConnectionError as ce:
            print("Unable to connect to ipstack")
        except requests.HTTPError as he:
            print("Invalid HTTP response from ipstack")
        except requests.Timeout as to:
            print("Timed out while connecting to ipstack. Try again later")
        except requests.TooManyRedirects as tmr:
            print("Too many redirects issued")

    def geolocate_ips_from_list(self):
        # If this is a tsv or csv output, the first thing we do is output the columns.
        self.is_column = True
        if not self.hide_column:
            print(self.get_columns())
        self.is_column = False
        # And then we open the input file for reading, followed by the output file.
        try:
            with open(self.input_file, "r") as file, open(str(time.strftime("%Y-%m-%d-%H-%M-%S") + "." +
                                                              self.output_format), "a") as self.file_handle:
                # We want unique IPs.
                lines = list(set(file.readlines()))
                for ip in lines:
                    self.output_list = []
                    self.short_list = []
                    r = self.make_request(ip)

                    # Looks like the request resulted in an HTTP status code of 200. That's probably a good thing.
                    if r.status_code == 200:
                        # But let's see what kind of content is in that request...
                        self.check_content(r)
        except FileNotFoundError as fnfe:
            print(f"[?] [PEBKAC] {self.input_file} does not exist.")
            self.rage_quit()

        # Let's get all the data from the JSON blobbery and store it somewhere. Like right here.

    # This will print the columns, or the rows.
    def get_columns(self):
        if self.output_format is not "json":
            for separator, format_type in self.format_dict.items():
                if self.output_format == format_type:
                    return f"{separator}".join(map(str,
                                                   self.output_column_names
                                                   if self.full_output
                                                   else self.short_columns))

    def get_rows(self):
        if self.output_format is not "json":
            for separator, format_type in self.format_dict.items():
                if self.output_format == format_type:
                    return f"{separator}".join(map(str, self.output_list if self.full_output else self.short_list))

    def write_print(self, msg):
        self.file_handle.write(msg + "\n")
        print(msg)


if __name__ == "__main__":
    geo = NeoGeo()
