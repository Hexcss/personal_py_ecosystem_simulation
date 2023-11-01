import numpy as np

def get_wrapped_slice(arr, x_start, x_end, y_start, y_end):
  height, width = arr.shape[0], arr.shape[1]
  x_start, x_end = x_start % width, x_end % width
  y_start, y_end = y_start % height, y_end % height
  
  if x_start < x_end and y_start < y_end:
      return arr[y_start:y_end, x_start:x_end]
  else:
      # Handle wrap-around scenarios
      horizontal_slices = np.split(arr, [x_start], axis=1)
      vertical_slices = np.split(arr, [y_start], axis=0)
      return np.vstack((vertical_slices[-1], vertical_slices[0]))[:, x_start:] if y_start > y_end else np.vstack((vertical_slices[0], vertical_slices[1]))[:, x_start:]
