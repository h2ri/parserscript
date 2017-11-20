import pdfplumber
import re
PATH_TO_FILE = "/Users/healthi/Downloads/AMANJYOTH SINGH SURI.PDF"
END_OF_PAGE = "---End Of Report---"

def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

pdf = pdfplumber.open(PATH_TO_FILE)
#p0 = pdf.pages[4] #works
p0 = pdf.pages[8]
p0 = p0.crop((6,290,600,800))
text = p0.extract_text()
report_list = text.split("\n")
final_result = {}
header_name = ["CREATININE, SERUM", "LIPID PROFILE", "LIVER FUNCTION TESTS (LFT)" ]
test_name = ["CREATININE-SERUM/PLASMA", "CHOLESTEROL", "HDL", "TRIGLYCERIDES", "LDL", "VLDL", "TOTALCHOLESTEROLHDLCHOLESTEROLRATIO"]
final_result = {}
header = ""
print(len(report_list))
previous_result = ""
for i in range(0,len(report_list)):
    if i == END_OF_PAGE:
             break
    print(report_list[i])
    print("\n")
    result_row = report_list[i]
    if result_row in header_name:
        header = result_row
        final_result[result_row] = {}
        result = {}
        continue
    split_grouping = result_row.split(" ")
    test_match_name = ""
    for j in split_grouping:
        result = {}
        test_match_name = test_match_name + j
        if re.search('^Method' ,test_match_name):
            result["Method"] = split_grouping
            try:
                final_result[header][previous_result].update(result)
            except KeyError:
                pass
            break
        if test_match_name in test_name:
            previous_result = test_match_name
            result[test_match_name] = {"Test_row" : split_grouping, "unit": split_grouping[-1:]}
            final_result[header].update(result)
            break
print("\n")
pretty(final_result)
# for i in list:
#     if i == "---End Of Report---":
#         break
#     result = {}
#     result["Test Name"] = i
#     split_grouping = i.split(" ")
#     test = ""
#     result["units"] = split_grouping[-1:]
#
#     for j in split_grouping:
#          test = test + j
#          # if test == "Method:":
#          #    print("in")
#          #    result["Method"] = i
#          #    print(list[-1])
#          #    #final_result[i-1] = result
#          #    break
#          if test == "Hemoglobin":
#             result["Test Name"] = test
#             print(split_grouping)
#             #result["units"] = split_grouping[-1:]
#             #name_end = split_grouping.index[i]
#             #variable_list = split_grouping[name_end+1:]
#     final_result[i] = result
#     #Group method
# pretty(final_result)
