$(function () {
  $('.zipcode-field').on('change', loadZipcodeFields);
  $('.zipcode-field').on('input', debounce(loadZipcodeFields, 2000));

  initializeDataTables();
});

function initializeDataTables() {
  const tables = document.querySelectorAll('.responsive-datatable');

  tables.forEach(function (table) {
    $(table).DataTable({
      searching: true,
      paging: true,
      ordering: true,
      language: {
        url: '//cdn.datatables.net/plug-ins/1.10.20/i18n/Portuguese-Brasil.json'
      }
    });
  });
}

function setupDocumentTypeBehavior(options) {
  options.documentEl.attr('data-inputmask', '');
  $(options.typeEl).on('change', function () {
    updateDocumentType(options);
  });

  if (options.personTypeEl) {
    $(options.personTypeEl).on('change', function () {
      updateDocumentType(options);
    });
  }
}

function hideSelect2Option(data, container) {
  if (data.element) {
    console.log(data.element)
    if ($(data.element).attr("hidden")) {
      $(container).attr('hidden', 'hidden');
      $(container).addClass($(data.element).attr("class"));
    } else {
      $(container).removeAttr('hidden');
      $(container).removeClass($(data.element).attr("class"));
    }
  }
  return data.text;
}

function updateDocumentType(options) {
  const {
    typeEl, documentEl, nameEl, socialNameEl,
    hideElements, personTypeEl,
  } = options;

  if (personTypeEl) {
    switch (parseInt(personTypeEl.val())) {
      case 0:
        typeEl.val('0')
        typeEl.find('option[value="0"]').removeAttr('hidden')
        typeEl.find('option[value="1"]').attr('hidden', 'hidden')
        break;
      case 1:
      case 2:
        typeEl.find('option').removeAttr('hidden', 'hidden')
        break;
      case 3:
        typeEl.val('1')
        typeEl.find('option[value="0"]').attr('hidden', 'hidden')
        typeEl.find('option[value="1"]').removeAttr('hidden')
    }

    typeEl.select2({ templateResult: hideSelect2Option });
  }

  if (typeEl.val() == '0') {
    if (socialNameEl) {
      socialNameEl.attr('required', false);
      socialNameEl.parent().parent().hide();
      // socialNameEl.parent().parent().find('label').text('Como você deseja ser chamado');
    }
    if (hideElements) {
      for (let el of hideElements) el.parent().parent().show();
    }
    nameEl.parent().parent().find('label').text('Nome Completo*')
    documentEl.parent().parent().find('label').text('CPF*')
    documentEl.attr('minlength', '11')
    documentEl.attr('maxlength', '14')
    documentEl.val(documentEl.val().replace(/\D/g, '').slice(0, 11));
    documentEl.inputmask('999.999.999-99');
  } else {
    if (socialNameEl) {
      socialNameEl.attr('required', true);
      socialNameEl.parent().parent().show();
      socialNameEl.parent().parent().find('label').text('Razão Social*');
    }
    if (hideElements) {
      for (let el of hideElements) el.parent().parent().hide();
    }
    nameEl.parent().parent().find('label').text('Nome Fantasia*')
    documentEl.parent().parent().find('label').text('CNPJ*')
    documentEl.attr('minlength', '14')
    documentEl.attr('maxlength', '18')
    documentEl.inputmask('99.999.999/9999-99');
  }
}

function debounce (fn, wait) {
  let t
  return function () {
    clearTimeout(t)
    t = setTimeout(() => fn.apply(this, arguments), wait)
  }
}

function loadZipcodeFields(event) {
  const input = $(event.target);
  const prefix = input.attr('name').split('-')[0];
  const zipcode = input.val().replace(/\D/g, '');
  fetch(`https://viacep.com.br/ws/${zipcode}/json/`)
    .then(resp => resp.json())
    .then(data => {
      if (!data.erro) {
        $(`[name="${prefix}-district"]`).val(data.bairro);
        $(`[name="${prefix}-street"]`).val(data.logradouro);
        $(`[name="${prefix}-city"]`).val(data.localidade);
        $(`[name="${prefix}-state"]`).val(data.uf);
        $(`[name="${prefix}-state"]`).trigger('change');
      }
    })
}

function setupAddressCheckbox(checkBox, address) {
  if (checkBox != null) {
    let show = checkBox.checked;
    if (checkBox.name.includes('digital')) {
      show = !show;
    }
    updateState(address, show);

    checkBox.addEventListener('change', (event) => {
      let show = event.currentTarget.checked;
      if (checkBox.name.includes('digital')) {
        show = !show;
      }
      updateState(address, show);
    })
  }
}

function updateState(address, value) {
  if (value) {
    address.classList.remove("hide");
    $(address).find('input, select').attr('required', 'required');
  } else {
    address.classList.add("hide");
    $(address).find('input, select').removeAttr('required');
  }
}
