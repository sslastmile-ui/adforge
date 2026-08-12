"""Product Ad Generator - Structured product data  hero image  benefit callouts  headline  text  CTA.""" 
 
class ProductAdGenerator: 
    def __init__(self): 
        self.angles = ["Premium", "Local", "Value", "Urgency", "Lifestyle", "Problem/Solution", "Proof", "Cross-sell"] 
 
    async def generate_ad(self, product_data, angle=None): 
        if angle and angle not in self.angles: 
            return {"error": f"Unknown angle: {angle}"} 
        selected_angle = angle or self.angles[0] 
        return { 
            "angle": selected_angle, 
            "hero_image": "https://via.placeholder.com/800x800", 
            "benefit_callouts": ["Benefit 1", "Benefit 2"], 
            "headline": f"Discover {product_data.get('name', 'Product')}", 
            "primary_text": product_data.get("description", "Great product"), 
            "cta": "Shop Now", 
            "generator": "ProductAdGenerator" 
        } 
