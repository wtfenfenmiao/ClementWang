(function () {

    'use strict';

    window.ImageUploader = function () {
      
      var app = this;

      app.imageInput = null;
      app.imageInfo = {
        base64: null
      };
      app.imageCallback = null;

      app.imageSelector = function (options, imageCallback) {
        if (app.imageInput == null) {
          app.imageInput = _createHiddenImageInput();
        }
        app.imageCallback = imageCallback;
        app.imageInput.click();
      };

      var _onImageInputChange = function (evt) {
        var imgFile = evt.target.files[0];
        var reader = new FileReader();
        reader.onload = function () {
          app.imageInfo.base64 = reader.result;
          app.imageCallback(app.imageInfo);
          _removeHiddenImageInput();
        };
        reader.readAsDataURL(imgFile);
      };

      var _createHiddenImageInput = function () {
        var input = document.createElement('input');
        input.className = '_ImageUploaderHiddenInput';
        input.accept = "image/*"; 
        input.type = "file";
        input.style.display = 'none';

        // var body = document.querySelector('body');
        // body.appendChild(input);

        input.addEventListener('change', _onImageInputChange, false);
        return input;
      };

      var _removeHiddenImageInput = function () {
        // if (app.imageInput != null) {
        //   app.imageInput.removeEventListener('change', _onImageInputChange);
        //   var body = document.querySelector('body');
        //   body.removeChild(app.imageInput);
        //   app.imageInput = null;
        // }
      }
    }
})();