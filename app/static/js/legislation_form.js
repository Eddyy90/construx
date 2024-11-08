$(function () {
  $('.search-legislation').on('change', loadSearchLegislation);
  $('.search-legislation').on('input', debounce(loadSearchLegislation, 2000));
});

function loadSearchLegislation(event) {
  const input = $(event.target);
  const prefix = input.attr('name').split('-')[0];
  const zipcode = input.val().replace(/\D/g, '');

  const number = ($(`[name="${prefix}-number"]`).val() || '').replace(/\D/g, '');
  const year = ($(`[name="${prefix}-year"]`).val() || '').replace(/\D/g, '');

  fetch(`/inquiry/search_legislation/?number=${number}&year=${year}`)
    .then(resp => resp.json())
    .then(data => {
      const pageUrlEl = $(`[name="${prefix}-page_url"]`);
      if (data.response.docs) {
        pageUrlEl.html('');
        for (let doc of data.response.docs) {
          if (!doc.sig_tipo_ato.toLowerCase().includes('lei')) {
            continue;
          }
          pageUrlEl.append($('<option>', {
            value: doc.id,
            text: doc.dsc_ementa,
          }));
        }
      }
    })
}

function updateLegislationInputs(prefix) {
  // const codeEl = $(`[name="${prefix}-code"]`)
  const penalEl = $(`[name="${prefix}-penal"]`)
  const pageUrlEl = $(`[name="${prefix}-page_url"]`)
  const numberEl = $(`[name="${prefix}-number"]`)
  const yearEl = $(`[name="${prefix}-year"]`)
  const articleEl = $(`[name="${prefix}-article"]`)
  const treeContainer = $('<div class="article-tree-container my-2"><div><div></div>');
  const treeEl = $(`[name="${prefix}-article_tree"]`);
  treeEl.after(treeContainer);
  let tree = null;
  const formEl = pageUrlEl.parents('form');
  const submitBtn = formEl.find('button[type="submit"]');
  let articleData = null;
  submitBtn.attr('disabled', '');

  formEl.on('submit', function (event) {
      let treeData = tree.getCheckedNodes().map(id => {
        let data = tree.getDataById(id);
        return { id: data.id, parent: data.parent, path: data.id.split('-') };
      });
      treeEl.val(JSON.stringify(treeData));
  });

  function loadFieldsInfo() {
    const article = articleEl.val();

    if (articleData && articleData.number == parseInt(article)) {
      return;
    }

    submitBtn.attr('disabled', '');
    treeContainer.html($(`
    <div id="legislation-spinner" class="spinner-border text-primary m-1" role="status">
        <span class="sr-only">Loading...</span>
    </div>
    `));
    let code = penalEl.prop('checked') ? '0' : '';

    fetch(`/inquiry/fetch_article/?code=${code}&page_url=${pageUrlEl.val() || ''}&article=${article}`)
    // fetch(`/inquiry/fetch/${article}`)
      .then(resp => resp.json())
      .then(data => {
        articleData = data;
        if (data.children) {
          let container = $('<div></div>');
          treeContainer.append(container)
          tree = makeTreeData(container, data);
        }
        submitBtn.removeAttr('disabled');
        $('#legislation-spinner').remove()
        // submitBtn.html('Adicionar');
      });
  }


  articleEl.on('change', loadFieldsInfo);
  articleEl.on('input', debounce(loadFieldsInfo, 2000));

  function toggleCodeFields (penal) {
    const elements = [pageUrlEl, numberEl, yearEl];
    if (penal) {
      for (let el of elements) el.parents('.form-group').hide();
      pageUrlEl.val('');
    } else {
      for (let el of elements) el.parents('.form-group').show();
    }
  }

  toggleCodeFields(penalEl.prop('checked'));
  penalEl.on('change', (event) => {
    const penal = event.target.checked;
    toggleCodeFields(penal);
  });
}

function romanize(num) {
  var lookup = {M:1000,CM:900,D:500,CD:400,C:100,XC:90,L:50,XL:40,X:10,IX:9,V:5,IV:4,I:1},roman = '',i;
  for ( i in lookup ) {
    while ( num >= lookup[i] ) {
      roman += i;
      num -= lookup[i];
    }
  }
  return roman;
}

function makeTreeData(treeEl, data) {
  let treeData = [];

  if (data.enumeration) {
    treeData.push(...data.enumeration.map(v => parseArticlePartial(v, ['e'])));
  }

  if (data.children) {
    treeData.push(...data.children.map(v => parseArticlePartial(v, ['p'])));
  }

  return treeEl.tree({
    primaryKey: 'id',
    uiLibrary: 'bootstrap4',
    dataSource: treeData,
    checkboxes: true
  });
}

function parseArticlePartial(data, prefix=[]) {
  const { number, description } = data;
  let children = null;
  if (data.children) {
    children = data.children.map(v => parseArticlePartial(v, [...prefix, number]));
  } else if (data.enumeration) {
    children = data.enumeration.map(v => parseArticlePartial(v, [...prefix, number]));
  }
  return {
    id: `${[...prefix, number].join('-')}`,
    parent: prefix,
    text: description,
    // checked: false,
    children: children,
  }
}