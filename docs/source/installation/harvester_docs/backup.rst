## File grouping for file transfers

JobSpec and DBInterface provide a couple of functions which allow plugins to easily group input or output files and to keep track of status for each group. [This plugin](https://github.com/HSF/harvester/blob/master/pandaharvester/harvesterpreparator/dummy_preparator.py) shows how JobSpec functions are used, and [another plugin](https://github.com/HSF/harvester/blob/master/pandaharvester/harvesterstager/dummy_bulk_stager.py) shows how DBInterface functions are used.

### JobSpec Methods

**`def get_input_file_attributes(self, skip_ready=False)`**

This method returns a dictionary of input file attributes. The key of the dictionary is the logical file name (LFN) of the input file and the value is a dictionary of file attributes (fsize, guid, checksum, scope, dataset, attemptNr and endpoint). attemptNr show how many times the file was tried for the action such as checking and preparing. If skip_ready is set to True, files are ignored if they are already in ready state. Concerning file status see the next section.  

**`def get_output_file_specs(self, skip_done=False)`**

This method returns a list of output FileSpecs. If skip_done is set to True, files are ignored if they are already finished or failed. FileSpec.attemptNr shows how many times the file was tried for the action such as checking and staging out.

**`def set_groups_to_files(self, id_map)`**

To set group information to files. id_map is a dictionary of {identifier_string: {'lfns': [LFN, ...], 'groupStatus': status_string}. Identifier_string is the identifier of the file group, which contains files with the lfns, and can be an arbitrary string. Status_string can also be an arbitrary string, but groups are ignored for the file->group lookup once the status_string is set to 'failed'. 

**`def update_group_status_in_files(self, identifier_string, status_string)`**

This method updates status of the group. Status_string is explained in the set_groups_to_files method. 

**`def get_groups_of_input_files(self, skip_ready=False)`**

To get a dictionary of {identifier_string: a dictionary of the group information} for input files. If skip_ready is set to True, the method returns groups of the input files which are not in ready state, which could be useful in the check_status method of preparator plugins. Keys of the group information dictionary are groupStatus and groupUpdateTime which are updated when the `set_groups_to_files` or `update_group_status_in_files` method is called.

**`def get_groups_of_output_files(self)`**

This methods works for output files as get_groups_of_input_files(). It doesn't take an extra argument since finished or failed files are automatically removed.

<br>

### DBInterface Methods

Note that plugins can access the DB through the self.dbInterface member which is automatically installed by plugin_factory when plugins are instantiated.  

**`def get_files_with_group_id(self, identifier_string)`**

This method returns the list of FileSpecs which have the same group identifier and may belong to different jobs.

**`def set_file_group(self, file_specs, identifier_string, status_string)`**

This method sets group information (identifier and status) to files.

**`def get_object_lock(self, object_name, lock_interval)`**

This method locks an object for lock_interval sec. This could be useful for plugins to take an action exclusively in multi-threading environment.

**`def release_object_lock(self, object_name)`**

This method releases the lock for an object, so that another thread can take the exclusive action next. 

<br>

## Protection against double input file transfers
If multiple jobs are fetched and they use the same input files, preparatory triggers stage-in only for the first job while keeping the others on hold until input files are successfully transferred. First, file status is set to `to_prepare` for the first job and `preparing` doe the other jobs. Once the check_status method of preparator plugin returns True for a job, file status is changed to `ready`. If the file status changes from `preparing` it inherits the grouping information, which is explained in the above section, of the first job.

<br>


---

<br>

## Error reporting
### Payloads
Payloads can report errors by adding 'pilotErrorCode', 'pilotErrorDiag', 'exeErrorCode', and 'exeErrorDiag'
in the `workerAttributesFile`, which is explained in [this section](https://github.com/HSF/harvester/wiki/Agents-and-Plugins-descriptions#update-jobs), or something equivalent for each messenger plugin.

### Plugins
Plugins can report errors in their methods by calling
```python
from pandaharvester.harvestercore.pilot_errors import PilotErrors
jobSpec.set_pilot_error(PilotErrors.ERR_XYZ, diagnostic_message)
```
if those methods take JobSpec or a list of JobSpecs as input(s), or
```python
workSpec.set_pilot_error(PilotErrors.ERR_XYZ, diagnostic_message)
```
if those methods take WorkSpec or a list of WorkSpecs as input(s),
where `ERR_XYZ` is an error code defined in the [PilotErrors](https://github.com/HSF/harvester/blob/master/pandaharvester/harvestercore/pilot_errors.py) class and `diagnostic_message`
is a string of a diagnostic message. If a pilot error is set to a WorkSpec, all JobSpecs associated to
the WorkSpec inherit the pilot error unless they set own pilot errors.

Plugins can provide supplemental information of worker errors to jobs even if those jobs have own error codes.
```python
workSpec.set_supplemental_error(WorkerErrors.error_codes[ERROR_CODE], diagnostic_message)
```
which is propagated to jobSpec.supErrorCode and jobSpec.supErrorDiag. This is typically useful to give to jobs additional diagnostic information which may or may not be directly related to the jobs. Error codes are defined in [WorkerErrors](https://github.com/HSF/harvester/blob/master/pandaharvester/harvestercore/worker_errors.py).

<br>

---

<br>

## Pilot closed
JobSpec and WorkSpec have the `set_pilot_closed()` method to report jobs as **closed** instead of **failed** to PanDA. This is typically useful to exclude harmless jobs from accounting, e.g. jobs which were prefetched but were then released since CPU slots were unavailable. Once set_pilot_closed() is called for a WorkSpec, set_pilot_closed() is automatically called for all JobSpecs associated to the WorkSpec. 

   

