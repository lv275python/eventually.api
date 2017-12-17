const max_image_size = 8*1024*1024;
const possible_image_types = ['gif', 'png', 'jpg', 'jpeg', 'bmp'];

const imageValidator = (imageType, imageSize) => {
    if (possible_image_types.includes(imageType) && imageSize<max_image_size) {
        return true;
    } else {
        return false;
    }
};

export {imageValidator};
