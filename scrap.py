results = [(1, "19-12-2011", "Comment"), (1, "19-12-2011", "Comment"), (1, "19-12-2011", "Comment"), (1, "19-12-2011", "Comment")]

for row in results:
    line = "<tr>"
    for item in row:
        line += "<td>" + str(item) + "</td>"
    line += "</tr>"
    print(line)
