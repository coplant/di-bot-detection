// обходит
export function checkImages() {
    let image = new Image();
    image.onload = function () {
        if (image.width > 0) {
            return true;
        }
    };
    image.src = 'px.png';
    return false;
}