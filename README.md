## tofd-scans-analysis
The analysis of the indications evaluation of welding imperfections using TOFD technic. An application automating analysis of ultrasound scans. Using: Python, OpenCV, Tkinter

### 7/9 accuracy

* finds 7/9 indications using *program_settings.txt*, displays dimensions of the biggest one, saves all indications to *results_in_mm.txt*

* **copy_list_without_one_elem(), do_overlap(), do_overlap_whole_list(), check_recs_over_recs()** - not used, to delete

* **discard_irrelevant_results()** improved with coefficient of variation (deviation/average_field and find_smallest_rec() )

* **check_histograms()** working like 75%, not satisfactory

* **find_roi()** improved by morphological transformations - static roi will be no longer supported

* **convert_to_mm() and confirm_indications()** - new features

* **inspect()** inproved by dilating and closing roi only and eroding whole image

* STILL A MESSY SPAGHETTI 
