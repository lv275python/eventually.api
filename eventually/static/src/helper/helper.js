export const s3Root='https://s3.eu-west-2.amazonaws.com/eventually-photos/';

export function getImageUrl(imageName){
    return s3Root + imageName;
}
