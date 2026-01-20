# Refactor message wrapper for improved rendering performance

Restructure chat message rendering to improve recycling performance by splitting generic wrapper into type-specific components, reducing prop drilling via Context, and optimizing list rendering.