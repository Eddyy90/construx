
function setupCkeditorLight (element, customOptions = null) {
  const options = {
    width: null,
    height: 90,
    indentation: '160px',
    mode: null,
    ...customOptions,
  }
  const { width, height, indentation, mode } = options;
  const config = {
    skin: 'moono-lisa',
    width: width,
    height: height,
    // Make the editing area bigger than default.
    extraPlugins: 'pastebase64,lineheight,textindent,pagebreak',
    // allow any tag, style and attr
    allowedContent: true,
    // tabSpaces: 4,
    indentation: indentation,
    autoParagraph: false, // stops automatic insertion of <p> on focus
    removePlugins : 'elementspath',

    // Since we define all configuration options here, let's instruct CKEditor 4 to not load config.js which it does by default.
    // One HTTP request less will result in a faster startup time.
    // For more information check https://ckeditor.com/docs/ckeditor4/latest/api/CKEDITOR_config.html#cfg-customConfig
    customConfig: '',

    // Upload images to a CKFinder connector (note that the response type is set to JSON).
    uploadUrl: null,

    // Configure your file manager integration. This example uses CKFinder 3 for PHP.
    // filebrowserBrowseUrl: '/apps/ckfinder/3.4.5/ckfinder.html',
    // filebrowserImageBrowseUrl: '/apps/ckfinder/3.4.5/ckfinder.html?type=Images',
    // filebrowserUploadUrl: '/apps/ckfinder/3.4.5/core/connector/php/connector.php?command=QuickUpload&type=Files',
    // filebrowserImageUploadUrl: '/apps/ckfinder/3.4.5/core/connector/php/connector.php?command=QuickUpload&type=Images',
    filebrowserBrowseUrl: null,
    filebrowserImageBrowseUrl: null,
    filebrowserUploadUrl: null,
    filebrowserImageUploadUrl: null,

    // For more information check:
    //  - About Advanced Content Filter: https://ckeditor.com/docs/ckeditor4/latest/guide/dev_advanced_content_filter.html
    //  - About Disallowed Content: https://ckeditor.com/docs/ckeditor4/latest/guide/dev_disallowed_content.html
    //  - About Allowed Content: https://ckeditor.com/docs/ckeditor4/latest/guide/dev_allowed_content_rules.html
    disallowedContent: 'img table',

    /*********************** File management support ***********************/
    // In order to turn on support for file uploads, CKEditor 4 has to be configured to use some server side
    // solution with file upload/management capabilities, like for example CKFinder.
    // For more information see https://ckeditor.com/docs/ckeditor4/latest/guide/dev_ckfinder_integration.html

    // Uncomment and correct these lines after you setup your local CKFinder instance.
    // filebrowserBrowseUrl: 'http://example.com/ckfinder/ckfinder.html',
    // filebrowserUploadUrl: 'http://example.com/ckfinder/core/connector/php/connector.php?command=QuickUpload&type=Files',
    /*********************** File management support ***********************/

    // An array of stylesheets to style the WYSIWYG area.
    // Note: it is recommended to keep your own styles in a separate file in order to make future updates painless.
    contentsCss: [
      // 'http://cdn.ckeditor.com/4.16.1/full-all/contents.css',
      '/static/libs/%40ckeditor/ckeditor4/contents.css',
    ],

    // This is optional, but will let us define multiple different styles for multiple editors using the same CSS file.
    bodyClass: 'document-editor',

    // Reduce the list of block elements listed in the Format dropdown to the most commonly used.
    format_tags: 'p;h1;h2;h3;pre',

    // Simplify the Image and Link dialog windows. The "Advanced" tab is not needed in most cases.
    removeDialogTabs: 'image:advanced;link:advanced',

    // Define the list of styles which should be available in the Styles dropdown list.
    // If the "class" attribute is used to style an element, make sure to define the style for the class in "mystyles.css"
    // (and on your website so that it rendered in the same way).
    // Note: by default CKEditor looks for styles.js file. Defining stylesSet inline (as below) stops CKEditor 4 from loading
    // that file, which means one HTTP request less (and a faster startup).
    // For more information see https://ckeditor.com/docs/ckeditor4/latest/features/styles.html
    stylesSet: [
      /* Inline Styles */
      {
        name: 'Marker',
        element: 'span',
        attributes: {
          'class': 'marker'
        }
      },
      {
        name: 'Cited Work',
        element: 'cite'
      },
      {
        name: 'Inline Quotation',
        element: 'q'
      },

      /* Object Styles */
      {
        name: 'Special Container',
        element: 'div',
        styles: {
          padding: '5px 10px',
          background: '#eee',
          border: '1px solid #ccc'
        }
      },
      {
        name: 'Square Bulleted List',
        element: 'ul',
        styles: {
          'list-style-type': 'square'
        }
      }
    ],
    on: { 'instanceReady': configureInstance },
    toolbar: [
      // {
      //   name: 'document',
      //   items: ['Source']
      // },
      {
        name: 'history',
        items: ['Undo', 'Redo']
      },
      {
        name: 'basicstyles',
        items: ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript']
      },
    ],
  };

  if (mode == 'lite') {
    Object.assign(config, {
      enterMode: CKEDITOR.ENTER_BR, // pressing the ENTER KEY input <br/>
      shiftEnterMode: CKEDITOR.ENTER_P, //pressing the SHIFT + ENTER KEYS input <p>
    });
  }
  if (mode == 'mid') {
    config.toolbar.push(...midStyles);
  }
  if (mode == 'advanced') {
    config.toolbar.unshift({
      name: 'clipboard',
      items: ['PasteFromWord']
    });
    config.toolbar.push(...midStyles);
    config.toolbar.push(...advancedStyles);
  }

  CKEDITOR.replace(element, config);
  // element.querySelector('#cke_id_content').style.width = '';
}

const midStyles = [
  {
    name: 'paragraph',
    items: ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent']
  },
];
const advancedStyles = [
  {
    name: 'quote',
    items: ['Blockquote']
  },
  {
    name: 'align',
    items: ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock']
  },
  {
    name: 'links',
    items: ['Link', 'Unlink']
  },
  // {
  //   name: 'editing',
  //   items: ['Scayt']
  // },
];

function configureInstance (ev) {
  var editor = ev.editor,
    dataProcessor = editor.dataProcessor,
    htmlFilter = dataProcessor && dataProcessor.htmlFilter;

  // Out self closing tags the HTML4 way, like <br>.
  dataProcessor.writer.selfClosingEnd = '>';

  // do not include span
  var tags = ['p', 'ol', 'ul', 'li', 'h1', 'h2', 'h3', 'h4', 'br'];

  for (let tag of tags) {
    dataProcessor.writer.setRules(tag, {
      indent: true,
      breakBeforeOpen: true,
      breakAfterOpen: true,
      breakBeforeClose: true,
      breakAfterClose: true,
    });
  }

  dataProcessor.writer.setRules('span', {
    indent: true,
    breakBeforeOpen: false,
    breakAfterOpen: false,
    breakBeforeClose: false,
    breakAfterClose: false,
  });

}