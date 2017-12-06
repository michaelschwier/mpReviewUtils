The "testData" folder contains a synthetic mpReview-like directory structure for 
testing. The filenames and directory structure is a subset derived from the
PCAmpMRI data. Patient names have been changed and simplified. Contents of image
files have been deleted. Contents of segmentations files have been changed to 
very simple masks. 
By default the segmentation is a 2x2x2 image with label 1 for all voxels at (:,0,:)
and label 0 for all voxels at (:,1,:)
For the *WholeGland" segmentations all voxels have label 1
For *Empty" segmentations all voxels have label 0 (and should not be part of the 
parsing result)
For *MultipleLabels* segmentations voxels at (0,0,:) have label 2, voxels at (1,1,:)
have label 0, all others have label 1 (and should not be part of the parsing result)