def rerange(value, min0, max1, normalizedMin = 0, normalizedMax = 1):
  return normalizedMin + ((value - min0) * (normalizedMax - normalizedMin)) / (max1 - min0)

def weighted_mean(values, weights):
  weights_sum = sum(weights)
  values_per_weights = 0
  for i in range(len(values)):
    value = values[i]
    weight = weights[i]
    values_per_weights += (value * weight)
  return values_per_weights / weights_sum
