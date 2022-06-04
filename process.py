import os
import os.path
import subprocess

_SCRIPT_CMD = "cat"
_FMT = "{:>14} {:>14} {:>14} {:>14} {:>14}"

def processOutFile(outfilepath):
    s = subprocess.run(args=[_SCRIPT_CMD, outfilepath],
                       text=True, capture_output=True)
    total_sum = 0
    main_sum = 0
    headers_past = False
    for l in s.stdout.splitlines():
        if headers_past:
            cols = l.split()
            total_sum += int(cols[0])
            main_sum += int(cols[6])
        if "==" in l: headers_past = True
    return {'total_sum': total_sum, '#main_sum': main_sum}

def processDir(dirname):
    # print("Processing:", dirname)
    results = {}
    for d in os.scandir(dirname):
        if not d.is_dir(): continue
        # print("Design:", d.name)
        for dout in os.scandir(d.path):
            if dout.is_file and dout.name.endswith(".nwcopt.out"):
                results[d.name] = processOutFile(dout.path)
                break
    return results

cwd_items = os.scandir()
base_dir = ""
test_dir = ""
for i in cwd_items:
    if i.is_dir() and i.name.endswith("_base"):
        base_dir = i.name
    elif i.is_dir() and i.name.endswith("_test"):
        test_dir = i.name

# print ("Base directory:", base_dir)
# print ("Test directory:", test_dir)

base_result = processDir(base_dir)
test_result = processDir(test_dir)

print(_FMT.format("design", "base_total", "base_main_sum", "test_total", "test_main_sum"))
lines = ["============"] * 5
print(_FMT.format(*lines))
for design in base_result:
    outs = [design, base_result[design]['total_sum'], base_result[design]['#main_sum']]
    if design in test_result:
        outs.append(str(test_result[design]['total_sum']))
        outs.append(str(test_result[design]['#main_sum']))
    else:
        outs.append(test_result[design]['n/a'])
        outs.append(test_result[design]['n/a'])
    print(_FMT.format(*outs))
