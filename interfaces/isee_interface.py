"""
Brief    : The interface class for the modules of vision algorithm used in ISEE.
VersIon  : 0.1
Date     : 2020.01.19
Copyright: ISEE, CRIPAC
"""

import abc

class ISEEVisAlgIntf(metaclass=abc.ABCMeta):

    # Error Code
    _isee_errors = {
        'success': 0,         # Success
        'no_such_file': -1,   # File is not existed
        'null_data': -2,      # Null data
        'null_predictor': -3, # Null predictor
        'bad_device_id': -4,  # Bad device index
        'not_support': -5     # Not supported operation
        }

    @classmethod
    def verson(self):
        return "Verson 0.1"

    @classmethod
    def getErrType(self, err_no):
        for err_type, err_val in self._isee_errors.items():
            if err_no == err_val:
                return err_type
        # No such error nomuber.
        print("ERROR: Bad error code!")
        return None

    @abc.abstractmethod
    def init(self, config_file, params_dict=None):
        """
        Load model.
        params:
          config_file: the path of the cofiguration file containing the 
          necessary parameters (e.g., XML, json, YAML etc.).
          params_dict: the necessary parameters to initialize the project.
          It is in the type of dictionary as follows:
          {
            gpu_id: [-1], # the gpu id (a list of Integers), -1 means using CPU.
            model_path: ['/home/yourmodelpath', ..., ''], # a list of strings.
            reserved: {}  # other necessary parameters.
          }
        note:
          If overlapping prameters are existed in the configuration file and
          the variable of params_dict, the parameters in the variable of 
          params_dict will be used.
        return:
          error code: 0 for success; a negative number for the ERROR type.
        """
        pass

    @abc.abstractmethod
    def process(self, imgs_data, **kwargs):
        """
        Inference through loaded model.
        params:
          imgs_data: a list images data to process.
          **kwargs : the necessary parameters to implement inference combining
                     the results of other tasks.
        return:
          error code: 0 for success; a negative number for the ERROR type.
        """
        pass

    @abc.abstractmethod
    def getResults(self):
        """
        Get the processing results.
        params:
        return:
          The processing results. None without calling the function of process.
        """
        pass

    @abc.abstractmethod
    def release(self):
        """
        Release the resources.
        """
        pass
