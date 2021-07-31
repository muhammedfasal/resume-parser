import json
import argparse
import pdfplumber


def json_writer(data, output_file):
    """write extracted data in to json file"""
    with open(output_file, "w") as outfile:
        json.dump(data, outfile)


def main(input_file, output_file):
    """main function that extract the content"""
    data = {}
    levels = {}
    content_list = []
    lines = 1
    pdf = pdfplumber.open(input_file)
    page = pdf.pages[0]
    text = page.extract_text()
    content_level = text.split("\n")
    content_level = [data.strip() for data in content_level if data.strip()]
    for content in content_level:
        if "____" in content:
            lines += 1
            content_list = []
        else:
            level = "level_" + str(lines)
            content_list.append(content)
            levels[level] = content_list
    for key, value in levels.items():
        if key == "level_1":
            data["name"] = levels["level_1"][0]
            address_ = levels["level_1"][1]
            address_ = address_.split("|")
            address_ = [x.strip() for x in address_ if x.strip()]
            address = address_[0] + "," + levels["level_1"][2]
            data["address"] = address
            email = address_[-1]
            data["email"] = email
            next_key = levels["level_1"][-1]
        else:
            temp = value[-1]
            del value[-1]
            data[next_key] = " ".join(value)
            next_key = temp
    data = {key: " ".join(value.split()) for key, value in data.items()}
    data = {key: value.replace("\u200b,", "") for key, value in data.items()}
    pdf.close()
    json_writer(data, output_file)
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    input_file = args.input
    output_file = args.output
    main(input_file, output_file)
