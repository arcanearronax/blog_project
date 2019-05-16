function updateBody(link) {
  console.log('updateBody - ' + link.id);
  document.getElementById("id_hide").checked = 0;
  document.getElementById("id_post_id").value = -1;
  document.getElementById("cat_id").value = -1;
  document.getElementById("id_title").value = '';
  document.getElementById("id_text").value = '';
  document.getElementById("id_desc").value = '';
  if (link.id == "NewPost") {
    document.getElementById("PostDiv").style.display = '';
    document.getElementById("PostFormDiv").style.display = '';
    document.getElementById("PostSelectDiv").style.display = 'none';
    document.getElementById("CatDiv").style.display = 'none';
  } else if (link.id == "EditPost") {
    document.getElementById("PostSelect").value = '';
    document.getElementById("PostDiv").style.display = '';
    document.getElementById("PostFormDiv").style.display = '';
    document.getElementById("PostSelectDiv").style.display = '';
    document.getElementById("CatDiv").style.display = 'none';
    getCKEditor('id_text');
  } else  if (link.id == "NewCategory") {
    document.getElementById("PostDiv").style.display = 'none';
    document.getElementById("CatDiv").style.display = '';
    document.getElementById("CatFormDiv").style.display = '';
    document.getElementById("CatSelectDiv").style.display = 'none';
  } else if (link.id == "EditCategory") {
    document.getElementById("CatSelect").value = '';
    document.getElementById("PostDiv").style.display = 'none';
    document.getElementById("CatDiv").style.display = '';
    document.getElementById("CatFormDiv").style.display = '';
    document.getElementById("CatSelectDiv").style.display = '';
  } else {
    console.log('updateBody - FAILURE');
  }
}

function getPostInfo() {
  var selectPost = document.getElementById("PostSelect");
  var post_json = JSON.parse(document.getElementById('post-data').textContent);
  var title_arr = post_json['titles'];
  var text_arr = post_json['texts'];
  var cat_arr = post_json['cats'];
  console.log('getPostInfo - Index - ' + selectPost.selectedIndex);
  document.getElementById("id_post_id").value = selectPost.selectedIndex;
  document.getElementById("id_title").value = title_arr[selectPost.selectedIndex];
  document.getElementById("id_text").value = text_arr[selectPost.selectedIndex];
  CKEDITOR.instances['id_text'].setData(text_arr[selectPost.selectedIndex]);
  console.log('Text: ' + text_arr[selectPost.selectedIndex]);
  console.log('test');
  document.getElementById("id_cat").value = cat_arr[selectPost.selectedIndex];

  console.log(title_arr);
  console.log(text_arr);
  console.log(cat_arr);
}

function getCatInfo() {
  var selectCat = document.getElementById("CatSelect");
  var cat_json = JSON.parse(document.getElementById('cat-data').textContent);
  var desc_arr = cat_json['descs'];
  var hide_arr = cat_json['hides'];
  console.log('getCatInfo - Index - ' + selectCat.selectedIndex);
  document.getElementById("cat_id").value = selectCat.selectedIndex;
  document.getElementById("id_desc").value = desc_arr[selectCat.selectedIndex];
  document.getElementById('id_hide').checked = hide_arr[selectCat.selectedIndex];
}

function getCKEditor(id) {
  console.log('getCKEditor: ' + id);
  var t = document.getElementById(id);
  console.log('getCk id: ' + t.id);
  CKEDITOR.replace(t, {
    width: 600
    }
  );
}

function updateCKEditor(id, text) {
  console.log('updateCKEditor: ' + id);
}
