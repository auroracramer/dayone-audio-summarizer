import pytz
import json
import os
import sys
import zipfile
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from datetime import datetime
from tempfile import TemporaryDirectory
from punctuator import Punctuator
from gensim.summarization.summarizer import summarize

PUNCTUATOR_MODEL_FNAME = 'Demo-Europarl-EN.pcl'
PUNCTUATOR_MODEL_PATH = os.path.join(os.path.dirname(__file__), PUNCTUATOR_MODEL_FNAME)
PUNCTUATOR = None


def process_transcriptions(transcriptions):
    global PUNCTUATOR
    if PUNCTUATOR is None:
        PUNCTUATOR = Punctuator(PUNCTUATOR_MODEL_PATH)

    if type(transcriptions) == str:
        transcriptions = [transcriptions]

    punctuated_transcriptions = []
    for t in transcriptions:
        punctuated_transcriptions.append(PUNCTUATOR.punctuate(t))

    full_text = " ".join(punctuated_transcriptions)
    try:
        summary = summarize(full_text).replace("\n", " ")
    except ValueError:
        summary = full_text
    return full_text, summary


def process_export(zip_path, output_path):
    if not output_path:
        output_path = os.path.splitext(zip_path)[0] + '-summary.md'
    output_text = ""

    with TemporaryDirectory() as tmp_dir:
        with zipfile.ZipFile(zip_path, 'r') as f:
            f.extractall(tmp_dir)

        json_path = os.path.join(tmp_dir, "Journal.json")
        with open(json_path, 'r') as f:
            journal_obj = json.load(f)

        for entry in journal_obj["entries"]:
            # Get UUID for eventual databasing
            uuid = entry["uuid"]

            # Process date
            date_str = entry["creationDate"]
            if date_str[-1] != 'Z':
                raise ValueError("Creation time must be UTC.")
            date_str = date_str[:-1]
            tz = pytz.timezone(entry["timeZone"])
            dt = pytz.utc.localize(datetime.fromisoformat(date_str)).astimezone(tz)
            output_text += dt.strftime("%b %-d, %Y %-I:%M %p (%Z)\n")
            output_text += "=============================\n"

            # Process audio transcriptions
            transcriptions = []
            for a in entry["audios"]:
                t = a.get("transcription", "").strip()
                if t:
                    transcriptions.append(t)
            if not transcriptions:
                continue
            full_text, summary = process_transcriptions(transcriptions)

            output_text += "- Summary: " + summary + "\n"
            output_text += "- Transcription: " + full_text + "\n\n"

    with open(output_path, 'w') as f:
        f.write(output_text)


def parse_arguments(args):
    parser = ArgumentParser(sys.argv[0], description="Summarize exported DayOne journals",
                            formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument('zip_path', help='Path to exported DayOne journals.')
    parser.add_argument('output_path', nargs="?", default="", help='Path to output summary file.')

    return parser.parse_args(args)


def main():
    args = parse_arguments(sys.argv[1:])
    process_export(args.zip_path, args.output_path)


if __name__ == "__main__":
    main()