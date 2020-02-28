# ftdc-flywheel_data-modulation
GitHub Repository for Penn FTDC for Flywheel Specific scripts/gears/etc. This repository exists for the Penn FTD Center to utilize a wrapper for `fw-heudiconv` to 'modulate'/convert data into the BIDS format. A lot of new users using the resources that `fw-heudiconv` has to offer often get led to confusion, because there are many intermediate steps, and the steps are not concisely outlined in a beginner-friendly manner in available documentation. This repository is to lessen that liklihood of confusion, and to complete the necessary steps of `fw-heudiconv` on data sets in one step.

### About BIDS 
BIDS (Brain Imaging Data Structure) is a standard naming convention to specify the description of neuroimaging data in an organized filesystem hierarchy. It is a scientific community effort that was initiated during an INCF session at Stanford University, the intiative led by Chris Corgolewski. In the figure down below, you can see how neuroimaging images are re-organized by modalities in parent folders, and the files are renamed as such. The top level is a subject ID, the next level is an imaging session label, followed by the re-named files based on the modality. You can read more on the naming convention of the actual imaging files in the *Naming* Section of this README page.

![BIDS Conversion](https://bids.neuroimaging.io/assets/img/dicom-reorganization-transparent-white_1000x477.png)

#### Mission Statment of BIDS
The mission of BIDS is to make neuroimaging more acessible, shareable, and usable for researchers. There are three foundational principles that BIDS is founded upon to organize and distribute neuroimaging data.
  ###### (1) "To minimize complexity and facilitate adoption, reuse existing methods and technologies whenever possible."
  ###### (2) "Tackle 80% of the most commonly used neuroimaging data, derivatives, and models (inspired by the pareto principle)."
  ###### (3) "Adoption by the global neuroimaging community and their input during the creation of the specification is critical for the success of the project."
  
  ### `FW-Heudiconv`
`fw-heudiconv` is a wrapper on the `heudiconv` software, a flexible converter that organizes neuroimaging data into modality-tuned hierarchies that are described above in the figure. `fw-heudiconv` take `heudiconv` a step further by working on data that has been stored on FlyWheel (hence the `fw` prefix). It does this by user-directed naming schemes which are customizable through a .py file called a heuristic. 

### Heuristic:
A heuristic is a Python file (.py) that specifies a discrete set of rules for naming all the neuroimaging files in your dataset. The heuristic takes information from the image header, and it is up to the discretion of the user to choose fields in the header that best suit the plan of action of organizing the data. More information on this is written in the *Developing Your Heuristic* section. A downloadable heuristic template is available for download and customization in this repository. 
