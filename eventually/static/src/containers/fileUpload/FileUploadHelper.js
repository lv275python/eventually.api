const maxImageSize = 8*1024*1024;
const possibleImageTypes = ['gif', 'png', 'jpg', 'jpeg', 'bmp'];

const imageValidator = (imageType, imageSize) => {
    if (possibleImageTypes.includes(imageType) && imageSize<maxImageSize) {
        return true;
    } else {
        return false;
    }
};

export {imageValidator};
