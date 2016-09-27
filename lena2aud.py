import csv
import sys

from collections import deque

def rank_regions(lena_data):
    start = 0
    end = 12

    region_values = []
    window = lena_data[start:end]

    region_count = 0
    while end <= len(lena_data):
        ctc_cvc_avg_sum = 0
        ctc_sum = 0
        cvc_sum = 0
        awc_sum = 0
        for entry in window:
            ctc_cvc_avg = (float(entry[21]) + float(entry[24])) / 2.0
            ctc_cvc_avg_sum += ctc_cvc_avg
            ctc_sum += float(entry[21])
            cvc_sum += float(entry[24])
            awc_sum += float(entry[18])
        region_values.append((region_count, ctc_cvc_avg_sum/12, ctc_sum/12, cvc_sum/12, awc_sum/12))

        start += 1
        end += 1
        region_count += 1
        window = lena_data[start:end]

    ranked_regions = sorted(region_values,
                            key=lambda region: region[1],
                            reverse=True)
    return ranked_regions



five_min_ms = 300000


def rank_regions(lena_data):
    start = 0
    end = subregion_size

    region_values = []
    window = lena_data[start:end]

    region_count = 0
    while end <= len(lena_data):
        ctc_cvc_avg_sum = 0
        ctc_sum = 0
        cvc_sum = 0
        awc_sum = 0
        for entry in window:
            ctc_cvc_avg = (float(entry[21]) + float(entry[24])) / 2.0
            ctc_cvc_avg_sum += ctc_cvc_avg
            ctc_sum += float(entry[21])
            cvc_sum += float(entry[24])
            awc_sum += float(entry[18])
        region_values.append((region_count,
                              ctc_cvc_avg_sum/subregion_size,
                              ctc_sum/subregion_size,
                              cvc_sum/subregion_size,
                              awc_sum/subregion_size))

        start += 1
        end += 1
        region_count += 1
        window = lena_data[start:end]

    ranked_regions = sorted(region_values,
                            key=lambda region: region[3],
                            reverse=True)
    return ranked_regions


def filter_overlaps(ranked_regions, top_n):
    filtered_regions = []

    for region in ranked_regions:
        overlapped = False
        if not filtered_regions:
            filtered_regions.append(region)
            continue
        for index, filtered_region in enumerate(filtered_regions):
            if regions_overlap(region, filtered_region):
                overlapped = True
                break

        if not overlapped:
            filtered_regions.append(region)

        if len(filtered_regions) == top_n:
            return filtered_regions

def regions_overlap(region, filtered_region):
    if region[0] < filtered_region[0] + subregion_size and \
        region[0] >= filtered_region[0]:
        return True
    if region[0] > filtered_region[0] - subregion_size and \
        region[0] <= filtered_region[0]:
        return True
    return False


def to_audacity_labels(five_min_list):
    with open(output, "wb") as out:
        for clip in five_min_list:
            out.write("{:.6f} {:.6f} {}\n".format(clip.start_time, clip.end_time, clip.clip_tier))

def read_lena_csv():
    lena_data = []
    with open(input_csv, "rU") as input:
        reader = csv.reader(input)
        reader.next()
        for row in reader:
            lena_data.append(row)
    return lena_data

def output_audacity_labels(lena_data, ranked_regions, output):
    # ranked_deque = deque(ranked_regions)
    # curr_region = ranked_deque.popleft()

    ranked_indices = [region[0] for region in ranked_regions]

    with open(output, "wb") as output:
        for index, region in enumerate(lena_data):
            value = region[24]
            if index in ranked_indices:
                value += ":  RANK {}".format(ranked_indices.index(index)+1)
                if only_print_ranked:
                    output.write("{:.6f} {:.6f} {}\n".format(index * 5 * 60, (index + subregion_size) * 5 * 60, value))
                    continue
            if not only_print_ranked:
                output.write("{:.6f} {:.6f} {}\n".format(index*5*60, (index+1)*5*60, value))

if __name__ == "__main__":
    input_csv = sys.argv[1]
    output = sys.argv[2]

    top_n = int(sys.argv[3])

    subregion_size = int(sys.argv[4]) # in terms of how many 5min

    only_print_ranked = False
    if len(sys.argv) > 5:
        only_print_ranked = True

    lena_regions = read_lena_csv()

    ranked_regions = rank_regions(lena_regions)

    filtered_regions = filter_overlaps(ranked_regions, top_n)

    output_audacity_labels(lena_regions, filtered_regions, output)

    print