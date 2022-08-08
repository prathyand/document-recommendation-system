import * as React from 'react';
import { useState,useEffect } from 'react'
import Button from '@mui/material/Button';
import Snackbar from "@mui/material/Snackbar";
import MuiAlert, { AlertProps } from "@mui/material/Alert";

async function fetchProfile() {
  
    let base_url;
    // console.log(isThissearch,uritoload);
    base_url=`http://localhost:8002/userprofile/`
     
    const response = await fetch(base_url, {
      "method": "GET",
      });
    
    const body = await response.json();
    return body['profile'];
  
  }
// function TagsInput({accesstags,fetchedtags}){
    function TagsInput(){
    const [tags, setTags] = useState([])
    const [open, setOpen] = useState(false);
    const setUserprofile=()=>{
        fetchProfile().then((newtags)=>{setTags(newtags)});
      }
    // useEffect(() => accesstags(tags),[tags]);
    useEffect(() => {
        let ignore = false;
        if (!ignore) {
            setUserprofile();
          // setUserprofile();
    
        }
        return () => { ignore = true; }
        },[])

      const Alert = React.forwardRef(function Alert(props, ref) {
          return React.createElement(MuiAlert, Object.assign({ elevation: 6, ref: ref, variant: "filled" }, props));
      });
      
    // setTags([...tags, value])
    function handleKeyDown(e){
        if(e.key !== 'Enter') return
        const value = e.target.value
        if(!value.trim()) return
        setTags([...tags, value])
        e.target.value = ''
        
        
    }

    const handleClose = (event, reason) => {
      if (reason === "clickaway") {
          return;
      }
      setOpen(false);
  };

    const updatedProfile = async ()=>{
        console.log("trying to update ",tags);
        const requestOptions = {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 'tags':tags })
        };
        console.log(requestOptions);
        const response = await fetch(`http://localhost:8002/userprofile/`, requestOptions)
        const body = await response.json();
        if(!response.ok){
          return Promise.reject(body);
        }
        else{
          console.log("profile updated");
          setOpen(true);
        }
      }


    function removeTag(index){
        setTags(tags.filter((el, i) => i !== index))
    }

    return (
        <div>
        <div className="tags-input-container">
            { tags.map((tag, index) => (
                <div className="tag-item" key={index}>
                    <span className="text">{tag}</span>
                    <span className="close" onClick={() => removeTag(index)}>&times;</span>
                </div>
            )) }
            <input onKeyDown={handleKeyDown} type="text" className="tags-input" placeholder="Add a topic" />
        </div >
        <Button variant="contained"  color="secondary" onClick={updatedProfile}>Update</Button>
        <Snackbar open={open} autoHideDuration={2000} onClose={handleClose} anchorOrigin= {{horizontal: 'left',vertical: 'top'}}>
        <Alert onClose={handleClose} severity="success" sx={{ width: "100%" }}>
          Preferences Successfully updated!
        </Alert>
      </Snackbar>
        </div>
        
    )
}

export default TagsInput