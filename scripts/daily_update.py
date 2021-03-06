# Copyright 2015 Altova GmbH
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#	  http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
__copyright__ = 'Copyright 2015 Altova GmbH'
__license__ = 'http://www.apache.org/licenses/LICENSE-2.0'

import time, download_feeds, download_filings, build_secdb
import tickers_cik
import sys

def main():
	# Parse script arguments
	build_secdb.args = build_secdb.parse_args(daily_update=True)
	build_secdb.args.company_re = None
	build_secdb.args.sic = None
	build_secdb.args.form_type = None
	# Setup python logging framework
	build_secdb.setup_logging(build_secdb.args.log_file)
	
	if build_secdb.args.update_tickers:
		argp = tickers_cik.mk_arg_parser()
		opts = argp.parse_args(["update", "--now=logs/tickers","--db=%s" %build_secdb.args.db_name, "--tickers-from-db"])
		tickers_cik.update_cmd(opts)

	feeds = download_feeds.download_feeds()
	for feed in feeds:
		download_filings.download_filings(feed,build_secdb.args)
		build_secdb.build_secdb(feeds)

if __name__ == '__main__':
	start = time.clock()
	main()
	end = time.clock()
	print('Finished in ',end-start)
