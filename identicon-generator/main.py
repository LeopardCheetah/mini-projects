# See the Zine Paged Out #4 page 8,
# Generating Identicons from SHA-256 hashes

# idea: make a hexagon comb identificor sha thing

# 3-4-5-4-3 = 19 total combs + colors which can accomodate a bunch of hashes i guess maybe



#--------------------------------------------------------------



# Create SVG string - more examples here https://www.w3schools.com/graphics/svg_intro.asp
# apparently we need this xmlns clause so we'll keep it for now
svg = """
<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500">
  <rect width="500" height="500" style="fill:rgb(0,0,0)" />
  <text x="20" y="200" fill="yellow">Some simple text.</text>
</svg>
"""

# Write to a text file
with open('image.svg', 'w') as f:
    f.write(svg)