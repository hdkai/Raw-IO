# Rio
RAW and raster image IO.

## Grouping Algorithms
We have a growing list of requirements:

- Variable group sizes. We can't rely on a fixed number of brackets per group.
- Flash frames. We need photometric invariance.
- Exposure extrema. Furhter need for photometric invariance.
- Weak translation invariance. We need to accommodate small shifts.
- Feature sensitivity. We need to not group images with dissimilar features. Doors open and closed.
- Performance. We can't spend too much time evaluating image similarity.
