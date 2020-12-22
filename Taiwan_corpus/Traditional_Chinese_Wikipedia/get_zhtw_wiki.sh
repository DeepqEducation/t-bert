
set -e

lg=zh


WIKI_FILENAME=${lg}wiki-latest-pages-articles.xml.bz2
WIKI_DOWNLOAD_LINK=https://dumps.wikimedia.org/${lg}wiki/latest/$WIKI_FILENAME
OUTPUT_FILENAME=wikicorpus_${lg}_one_article_per_line.txt


if [ -f "bz2/${WIKI_FILENAME}" ]; then 
	echo "Found ${WIKI_FILENAME} in folder bz2, skip downloading process.\n"
else
	echo "${WIKI_FILENAME} not found in bz2/"
	echo "Downloading ${WIKI_DOWNLOAD_LINK}"
	wget -c $WIKI_DOWNLOAD_LINK -P bz2/
	echo "Downloaded $WIKI_FILENAME in bz2/$WIKI_FILENAME"
fi


if [ ! -d wikiextractor ]; then
    echo "Cloning WikiExtractor from GitHub repository..."
    git clone https://github.com/attardi/wikiextractor.git
else
    echo "Found WikiExtractor, skip cloning.\n"
fi


if [ -d extracted ]; then
	echo "Folder extracted is already exist, skip extract process.\n"
else
    echo "Extracting articles from ${WIKI_FILENAME}\n"
	python wikiextractor/WikiExtractor.py bz2/${WIKI_FILENAME} -b 100M --processes 8 -q -o extracted
fi


if [ -f "raw/${OUTPUT_FILENAME}" ]; then 
	echo "raw/${OUTPUT_FILENAME} is already exist, skip producing process.\n"
else
	echo "Clean article and produce raw/${OUTPUT_FILENAME}"
	mkdir -p raw
	python WikicorpusTextFormatting.py --wiki_path extracted --output_filename raw/${OUTPUT_FILENAME}
fi


if [ -f "final/${OUTPUT_FILENAME}" ]; then 
	echo "final/${OUTPUT_FILENAME} is already exist, skip converting process.\n"
else
	echo "Converting raw/${OUTPUT_FILENAME} into Traditional Chinese, and saved in final/${OUTPUT_FILENAME}"
	mkdir -p final
	opencc -i raw/${OUTPUT_FILENAME} -o final/origin_${OUTPUT_FILENAME} -c s2twp.json
fi

echo "Process complete!"
