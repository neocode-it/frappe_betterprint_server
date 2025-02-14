split_table_by_maxheight = """
(maxHeight) =>{
    const foot = document.querySelector('tfoot');
    const footHeight = foot ? foot.offsetHeight : 0;

    const head = document.querySelector('thead');
    const headHeight = head ? head.offsetHeight : 0;

    maxPixelHeight = maxHeight / 0.26458 - headHeight - footHeight;

    const elements = document.querySelectorAll('tbody tr')
    
    pages = [];
    currentPage = '';
    currentHeight = 0;
    currentItemCount = 0;
    
    elements.forEach(element => {
        elementHeight = element.offsetHeight;

        if(currentHeight + elementHeight > maxPixelHeight && currentHeight > 0){
            tablePage = document.querySelector("table").cloneNode(true);
            tablePage.querySelector("tbody").innerHTML = currentPage;
            pages.push({"content": tablePage.outerHTML, "item_count": currentItemCount});

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
        tablePage = document.querySelector("table").cloneNode(true);
        tablePage.querySelector("tbody").innerHTML = currentPage;
        pages.push({"content": tablePage.outerHTML, "item_count": currentItemCount});
    }
    return pages;
}
"""
"""JS Function

Arguments:      int `maxHeight`

Return value:   `[html]`"""

get_element_height = """
(selector) => {
    const elements = document.querySelectorAll(selector);
    const heights = [];
    elements.forEach(element => {
        heights.push(Math.round(element.offsetHeight * 0.26458));
    });
    return heights;
}
"""
"""JS Function

Arguments:      str `selector`

Return value:   `[height(s)]`"""


# Note: still experimental, not tested yet
split_text_by_maxheight = """
function adjustContent(maxHeight) {
    const inputDiv = document.getElementById('html-input');
    const outputDiv = document.getElementById('page-output');
    const elements = inputDiv.children;
    
    for (let i = 0; i < elements.length; i++) {
        outputDiv.appendChild(elements[i].cloneNode(true));
        
        if (outputDiv.offsetHeight > maxHeight) {
            let lastElement = outputDiv.lastElementChild;
            let lastElementClone = lastElement.cloneNode(false);
            let content = lastElement.innerHTML.split(' ');
            
            while (outputDiv.offsetHeight > maxHeight && content.length > 0) {
                lastElement.innerHTML = content.join(' ');
                lastElementClone.innerHTML = content.pop() + ' ' + lastElementClone.innerHTML;
            }
            
            outputDiv.removeChild(lastElement);
            outputDiv.appendChild(lastElementClone);
            break;
        }
    }
    
    return outputDiv.innerHTML;
}
"""


split_text_by_height = """
// Prototype
// Almost ready for prod
//
// Usage:     
// from betterprint_server.worker.js import split_text_by_height
// pages = page.evaluate(split_text_by_height, [task["max-height"], 67])

([selector, zwo]) => {
    function getNodes(element) {
        const elementNodes = [];
        element.childNodes.forEach(node => {
            if (node.nodeType === Node.ELEMENT_NODE) {
                elementNodes.push(node);
            }
        });
        return elementNodes;
    }
    function setParentTree(targetcontainer){
        targetcontainer.innerHTML = "";
        let currentNode = targetcontainer;
        
        if (currentParentTree.length > 0){
            currentNode = currentParentTree[0].cloneNode(false);
            targetcontainer.appendChild(currentNode);
        }
        
        for(let i=1; i<currentParentTree.length; i++){
            currentNode = currentParentTree[i-1].cloneNode(false);
            targetcontainer.appendChild(node);
        }

        return currentNode;
    }
    function limitText(itemNodes, testDiv, parentEl, maxHeight){
        for(let i=0; i<itemNodes.length; i++){

            element = itemNodes[i];
            const newel = element.cloneNode(true);
            
            parentEl.appendChild(newel);
            
            if(testDiv.offsetHeight > maxHeight){

                // Is the current item the only? 
                // -> Might be to large
                if (parentEl.childNodes.length == 1){
                    // Check if item can be split
                    const newNodes = getNodes(itemNodes[i]);
                    if (newNodes.length > 0){
                        // Remove previously added node
                        let newParent = parentEl.lastChild;
                        newParent.innerHTML = "";

                        // Use recursive split
                        currentParentTree.push(newParent);
                        limitText(newNodes, testDiv, newParent, maxHeight);
                        currentParentTree.pop();
                    }

                    else {
                        alert("Item to large");
                        break;
                    }
                } else {
                    document.querySelector("body").appendChild(testDiv.cloneNode(true));
                    // finish page
                    parentEl = setParentTree(testDiv);
                
                    // Set index -1 to re-take current item
                    i --;
                }
                
                
            }
            
        }

    }

    currentParentTree = [];

    const container = document.querySelector('.tester');
    const parent = document.querySelector("main");
    const nodes = getNodes(parent);
    parent.remove();
    limitText(nodes, container, container, 300);
    return zwo;
}
"""
