(function($) {
  function getCookie(name) {
    var m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return m ? decodeURIComponent(m.pop()) : '';
  }
  function adminRoot() {
    return window.location.pathname.replace(/\/\d+\/change\/?$/, '');
  }

  function attach(ctx) {
    $(ctx).find('tr.form-row').each(function() {
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

      if ($deleteCell.find('.js-inline-delete-now').length) {
        $row.data('instant-delete-added', true);
        return;
      }

      var $btn = $('<button type="button" class="button js-inline-delete-now">Удалить</button>');
      $btn.on('click', function() {
        var url = adminRoot() + '/inline-delete/' + pk + '/';
        fetch(url, {
          method: 'POST',
          headers: { 'X-CSRFToken': getCookie('csrftoken') }
        })
        .then(function(r) {
          if (!r.ok) return r.text().then(function(t){ throw new Error('HTTP '+r.status+': '+t.slice(0,200)); });
          return r.json();
        })
        .then(function() {
          $delCheckbox.prop('checked', true).trigger('change');
          $row.addClass('inline-marked-for-delete').hide();
        })
        .catch(function(err) {
          alert('Ошибка удаления: ' + err.message);
        });
      });

      $deleteCell.append($btn);
      $row.data('instant-delete-added', true);
    });
  }

  $(document).ready(function(){ attach(document); });
  $(document).on('formset:added', function(e, $row){ attach($row); });
})(django.jQuery);
