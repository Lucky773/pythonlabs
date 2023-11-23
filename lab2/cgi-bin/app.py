import cgi

form = cgi.FieldStorage()

tea_type = form.getvalue("tea_type")
extras = form.getlist("extras")
quantity = form.getvalue("quantity")

print("Content-type: text/html\n")
print("<html>")
print("<head><title>Магазин чаю</title></head>")
print("<link rel='stylesheet' href='../stylesheet/style.css'>")
print("<body>")
print("<center>")
print("<br>")
print("<h1>Ваше замовлення:</h1>")
print("<form>")
print("<p>Чай: {}</p>".format(tea_type))
print("<p>Додатки:")
for extra in extras:
    print("<br>{}".format(extra))
print("</p>")
print("<p>Кількість: {}</p>".format(quantity))
print("</form>")
print("</center>")
print("</body>")
print("</html>")
