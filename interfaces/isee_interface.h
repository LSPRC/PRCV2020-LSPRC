/** @brief  : the interface for the prediction algorithm.
 *  @Version: 0.1
 *  @Author : ISEE, CRIPAC
 *  @Date   : 2020/05/22
 */

#ifndef _ISEE_VISUAL_ALG_INTF_H_
#define _ISEE_VISUAL_ALG_INTF_H_

#include "basic_define.h"

/** @class: ISEEVisAlgIntf
 */
class ISEEVisAlgIntf {

  public:
    virtual ~ISEEVisAlgIntf() {}

    /**
     * \brief initialization.
     * \param[IN] config_file - the path for the configuration file.
     * \param[IN] argc - number of values in argv.
     * \param[IN] argv - parameters.
     * \return: a handle (a pointer to the inside object to achieve prediction)
     */
    virtual long init(const unsigned char* config_file, int argc, 
        char** argv) = 0;

    /** 
     * \brief prediction for one input image.
     * \param[IN] handle
     * \param[IN] img - the rgb data of input image with its basic information.
     * \return error code.
     */
    virtual int process(long handle, const ISEEInputIMG& img) = 0;

    /**
     * \brief prediction for a batch of images.
     * \param[IN] handle.
     * \param[IN] batchsize - number of input images.
     * \param[IN] imgs - an array of images.
     * \return error code.
     */
    virtual int process(long handle, int batchsize, ISEEInputIMG* imgs) = 0;

    /**
     * \brief get the analysis results.
     * \param[IN] handle
     * \param[IN] length - size of the outputs.
     * \return analysis results.
     */
    virtual const float* getResults(long handle, int& length) = 0;

    /**
     * \brief release the resources.
     * \param[IN] handle
     */
    virtual void release(long handle) = 0;

};

#endif // _ISEE_VISUAL_ALG_INTF_H_
