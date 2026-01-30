from browser import document, html

# Create a canvas element
canvas = html.CANVAS(width=200, height=200, style={"border":"1px solid black"})
document <= canvas  # add canvas to the page

# Get canvas context
ctx = canvas.getContext("2d")

# Draw a circle
ctx.beginPath()
ctx.arc(100, 100, 50, 0, 6.28319)  # x, y, radius, start angle, end angle (2*pi)
ctx.fillStyle = "red"
ctx.fill()
ctx.stroke()
