split_table_by_maxheight = '''
(maxHeight) =>{
    const foot = document.querySelector('tfoot');
    const footHtml = foot ? foot.outerHTML : '';
    const footHeight = foot ? foot.offsetHeight : 0;

    const head = document.querySelector('thead');
    const headHtml = head ? head.outerHTML : '';
    const headHeight = head ? head.offsetHeight : 0;

    maxPixelHeight = maxHeight / 0.26458 - headHeight - footHeight;

    const elements = document.querySelector('tbody') ? 
        document.querySelectorAll('tbody tr') : 
        document.querySelectorAll('tr');
    
    pages = [];
    currentPage = '';
    currentHeight = 0;
    currentItemCount = 0;
    
    elements.forEach(element => {
        elementHeight = element.offsetHeight;

        if(currentHeight + elementHeight > maxPixelHeight && currentHeight > 0){
            pages.push({"content": headHtml + currentPage + footHtml, "item_count": currentItemCount});

            currentItemCount = 0;
            currentHeight = 0;
            currentPage = '';
        }

        currentItemCount ++;
        currentPage += element.outerHTML;
        currentHeight += elementHeight;
    });

    // cleanup current page
    if(currentPage.length > 0){
        pages.push({"content": headHtml + currentPage + footHtml, "item_count": currentItemCount});
    }
    return pages;
}
'''
"""JS Function

Arguments:      int `maxHeight`

Return value:   `[html]`"""