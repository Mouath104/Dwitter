let Boxes = Array.from(document.querySelectorAll(".box"))
let f=1
let f2=0
Boxes.forEach(
    (ele)=>{
        ele.getElementsByTagName('div')[2].querySelector('span').addEventListener("click",Click_child)

        //This If block is to keep the flag 'f' updated when redirecting to the dashboard page so that users don't have to doulbe click to view the comment
        // if(ele.getElementsByTagName('div')[3].classList.contains("unfocused")){
        //     f=1
        // }else{
        //     f=0
        //     let f2=1
        // }
    }
)


function Click_child(){
    if(f){
        console.log(this.getAttribute("id"))
        Boxes.forEach(
            (ele)=>{
                if(ele.getAttribute("id")==this.getAttribute("id")){
                    ele.querySelector('.alter').classList.remove("unfocused")
                    console.log("removed")
                }
            }
        )
        f=0
    }
    else{
        console.log(this.getAttribute("id"))
        Boxes.forEach(
            (ele)=>{
                if(ele.getAttribute("id")==this.getAttribute("id")){
                    ele.querySelector('.alter').classList.add("unfocused")
                    console.log("added")
                }
            }
        )
        f=1
    }

}
