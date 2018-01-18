export const isObjectsEqual = (firstObj, secondObj) => {
    return (Object.keys(firstObj).map(key => {
        return firstObj[key] === secondObj[key];
    }).every(elem => elem === true));
};
