import csv
import sys

from collections import deque

#Creates list "ranked_regions" that is used in "filter_overlaps" function
def rank_regions(lena_data):
    #Initialize variables to be used
    start = 0
    end = 12

    region_values = []
    window = lena_data[start:end]

    region_count = 0
    #While loop runs until "end" variable is > length of lena_data
    #Can't run if end > length of lena_data because variable window is part of lena_data from start to end
    while end <= len(lena_data):
        #Initially set variables equal to zero
        ctc_cvc_avg_sum = 0
        ctc_sum = 0
        cvc_sum = 0
        awc_sum = 0
        #Loop through entries in window (splice of lena_data)
        for entry in window:
            ctc_cvc_avg = (float(entry[21]) + float(entry[24])) / 2.0
            ctc_cvc_avg_sum += ctc_cvc_avg
            ctc_sum += float(entry[21])
            cvc_sum += float(entry[24])
            awc_sum += float(entry[18])
        #Add variables and their newly assigned values to the list "region_values"
        region_values.append((region_count, ctc_cvc_avg_sum/12, ctc_sum/12, cvc_sum/12, awc_sum/12))

        #Increment start, end, region_count, and window variables
        start += 1
        end += 1
        region_count += 1
        window = lena_data[start:end]

    ranked_regions = sorted(region_values,
                            key=lambda region: region[1],
                            reverse=True)
    return ranked_regions



five_min_ms = 300000

#Creates list "ranked_regions" that is used in "filter_overlaps" function
def rank_regions(lena_data):
    #Initialize variables start, end, region_values, window, region_count
    start = 0
    end = subregion_size

    region_values = []
    window = lena_data[start:end]

    region_count = 0
    # While loop runs until "end" variable is > length of lena_data
    # Can't run if end > length of lena_data because variable window is part of lena_data from start to end
    while end <= len(lena_data):
        #Initialize variables to be updated and appended to region_values list
        ctc_cvc_avg_sum = 0
        ctc_sum = 0
        cvc_sum = 0
        awc_sum = 0
        #Loop through each entry in window list (splice of lena_data)
        for entry in window:
            #Update values of variables initially set to zero
            ctc_cvc_avg = (float(entry[21]) + float(entry[24])) / 2.0
            ctc_cvc_avg_sum += ctc_cvc_avg
            ctc_sum += float(entry[21])
            cvc_sum += float(entry[24])
            awc_sum += float(entry[18])
        #Append variables and their newly assigned values to the list "region_values"
        region_values.append((region_count,
                              ctc_cvc_avg_sum/subregion_size,
                              ctc_sum/subregion_size,
                              cvc_sum/subregion_size,
                              awc_sum/subregion_size))

        #Increment/Update variables start, end, region_count, and window for next run through the while loop
        start += 1
        end += 1
        region_count += 1
        window = lena_data[start:end]

    ranked_regions = sorted(region_values,
                            key=lambda region: region[3],
                            reverse=True)
    return ranked_regions


#Function uses ranked_regions list that was created by rank_regions function as a parameter
def filter_overlaps(ranked_regions, top_n):
    #Initialize filtered_regions variable to empty list
    filtered_regions = []

    for region in ranked_regions:
        #Initialize overlapped variable to boolean "False"
        overlapped = False
        if not filtered_regions: #region in question from ranked_regions is not in filtered_regions list
            filtered_regions.append(region) #Append this region to filtered_regions list
            continue
        for index, filtered_region in enumerate(filtered_regions):
            #Calls helper function "regions_overlap" on region from ranked_regions and region from filtered_regions
            if regions_overlap(region, filtered_region):
                overlapped = True #Update overlapped variable accordingly
                break

        if not overlapped:
            #If region from ranked_regions and filtered_region in question do not overlap
            #Append region from ranked_regions to filtered_regions list
            filtered_regions.append(region)

        #Maximum size of filtered_regions list is reached, return filtered_regions list and break out of the function
        if len(filtered_regions) == top_n:
            return filtered_regions

#Helper function called in "filter_overlaps" function
def regions_overlap(region, filtered_region):
    #Check if region starts after filtered_region and filtered_region + subregion_size extends past region[0]
    if region[0] < filtered_region[0] + subregion_size and \
        region[0] >= filtered_region[0]:
        return True
    #Check if region starts before filtered_region and filtered_region - subregion_size is less than region[0]
    if region[0] > filtered_region[0] - subregion_size and \
        region[0] <= filtered_region[0]:
        return True
    return False


#Write to the file entitled "out"
def to_audacity_labels(five_min_list):
    with open(output, "wb") as out:
        for clip in five_min_list:
            out.write("{:.6f} {:.6f} {}\n".format(clip.start_time, clip.end_time, clip.clip_tier))

#Function called in "__main__" method
def read_lena_csv():
    #Initialize list "lena_data" to empy list
    lena_data = []
    #Open file for reading
    with open(input_csv, "rU") as input:
        reader = csv.reader(input)
        reader.next()
        for row in reader:
            #Building up the lena_data list by appending rows from input_csv file
            lena_data.append(row)
    return lena_data

#Function called in "__main__" method
def output_audacity_labels(lena_data, ranked_regions, output):
    # ranked_deque = deque(ranked_regions)
    # curr_region = ranked_deque.popleft()

    #Initialize variable "ranked_indices" through use of "ranked_regions" list parameter
    ranked_indices = [region[0] for region in ranked_regions]

    #Open output file for writing
    with open(output, "wb") as output:
        #Loop through regions in lena_data list
        for index, region in enumerate(lena_data):
            value = region[24]
            if index in ranked_indices:
                value += ":  RANK {}".format(ranked_indices.index(index)+1)
                if only_print_ranked: #boolean variable initialized in "__main__" method
                    #Write to output file incorporating subregion_size (initialized in "__main__" method)
                    output.write("{:.6f} {:.6f} {}\n".format(index * 5 * 60, (index + subregion_size) * 5 * 60, value))
                    continue
            if not only_print_ranked:
                #Write to output file not incorporating subregion_size (initialized in "__main__" method)
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