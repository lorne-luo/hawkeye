function createCollectionChooser(id) {
  var chooserElement = $('#' + id + '-chooser');
  var input = $('#' + id);
  var editLink = chooserElement.find('.edit-link');

  $('#' + id + '_select', chooserElement).change(function () {
    input.val(this.value);
    if (this.value) {
      editLink.attr("href", editLink.data("url") + this.value + '/');
      editLink.show()
    } else {
      editLink.hide()
    }
  });
}
