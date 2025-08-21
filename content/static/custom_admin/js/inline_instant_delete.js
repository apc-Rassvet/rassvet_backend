(function($) {
  function getCookie(name) {
    var m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return m ? decodeURIComponent(m.pop()) : '';
  }
  function adminRootFromPath() {
    return window.location.pathname.replace(/\/\d+\/change\/?$/, '');
  }

  function attach(container) {
    $(container).find('tr.form-row').each(function() {
      var $row = $(this);
      if ($row.hasClass('empty-form')) return;
      if ($row.data('instant-delete-added')) return;

      var $idInput = $row.find('input[type=hidden][name$="-id"]');
      var pk = $idInput.val();
      if (!pk) return;

      var $deleteCell = $row.find('td.delete');
      if (!$deleteCell.length) $deleteCell = $row.find('td').last();

      var $delCheckbox = $row.find('input[type=checkbox][name$="-DELETE"]');
      $delCheckbox.closest('label').hide(); 
      $delCheckbox.hide();

      if ($deleteCell.find('.inline-instant-delete').length) return;

      var $btn = $('<button type="button" class="button inline-instant-delete">Удалить</button>');
      $btn.on('click', function() {
        var url = adminRootFromPath() + '/inline-delete/' + pk + '/';
        var fd = new FormData();
        var empId = $('#id_id').val();
        if (empId) fd.append('employee_id', empId);

        fetch(url, { method: 'POST', headers: { 'X-CSRFToken': getCookie('csrftoken') }, body: fd })
          .then(function(r){
            if (!r.ok) return r.text().then(function(t){ throw new Error('HTTP '+r.status+': '+t.slice(0,120)); });
            return r.json();
          })
          .then(function(){
            $delCheckbox.prop('checked', true).trigger('change');
            $row.addClass('inline-marked-for-delete').hide();
          })
          .catch(function(err){ alert('Ошибка удаления: ' + err.message); });
      });

      $deleteCell.append($btn);
      $row.data('instant-delete-added', true);
    });
  }

  $(document).ready(function(){ attach(document); });
  $(document).on('formset:added', function(ev, $row){ attach($row); });
})(django.jQuery);
