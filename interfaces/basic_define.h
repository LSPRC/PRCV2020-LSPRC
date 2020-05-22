/** @file basic_define.h
 *  @brief   Basic definition used in the code for LSPRC
 *  @author  CRIPAC
 *  @version 0.1
 *  @date    2020/05/22
 */

#ifndef _ISEE_BASIC_DEFINE_H_
#define _ISEE_BASIC_DEFINE_H_

/* Error list. */
enum ISEE_ErrorsList {
    SUCCESS = 0,
    LOAD_FILE_FAILED = -1,
    NULL_DATA = -2,
    NULL_PREDICTOR = -3,
    BAD_DEVICE_ID = -4,
    NOT_SUPPORT = -5,
};

/* Information of input image. */
typedef struct isee_input_image_t {
    int img_w;
    int img_h;
    int num_channels;
    unsigned char* img_data;  // bgr, bgr, ...
} ISEEInputIMG;

/* Bounding box. */
typedef struct isee_bounding_box_t {
    int top;
    int left;
    int bottom;
    int right;
} ISEEBoundingBox;

#endif  // _ISEE_BASIC_DEFINE_H_
