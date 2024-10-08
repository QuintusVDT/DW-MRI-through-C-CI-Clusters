from dipy.io.streamline import load_tractogram, save_tractogram
import numpy as np

trk_file = "/globalscratch/users/d/u/dujardin/studies/study/subjects/IRM_102202_E1/dMRI/tractography/tois/IRM_102202_E1_cst_right_cross.trk"

trk = load_tractogram(trk_file, 'same')
trk.to_vox()
trk.to_corner()

streams_data = trk.streamlines.get_data()

b = np.float64(streams_data)

print(b)
print(trk.streamlines._offsets)
print(np.shape(b))
print(len(trk.streamlines._offsets))