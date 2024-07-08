
def calculate_api_price(response_data):
    input_price_per_million = 15
    output_price_per_million = 75

    usage_data = response_data.get('usage', {})
    input_tokens = usage_data.get('input_tokens', 0)
    output_tokens = usage_data.get('output_tokens', 0)

    input_price = input_tokens / 1_000_000 * input_price_per_million
    output_price = output_tokens / 1_000_000 * output_price_per_million
    total_price = input_price + output_price
    total_tokens = input_tokens + output_tokens

    return total_price, input_tokens, input_price, output_tokens, output_price, total_tokens
