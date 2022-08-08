import React from 'react';
import './App.css';
import 'rc-slider/assets/index.css';
import Button from './Button';
import RecipeReviewCard from "./card"
import FeedSelectFilter from './recom_algo_filters'
import Snackbar from "@mui/material/Snackbar";
import MuiAlert from "@mui/material/Alert";
import Item from "./Item"


 async function postClickEvent(keyid,eventType){
  let ts = new Date(Date.now())
  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ keyid: keyid, interaction_type:eventType,interaction_timestamp:ts})
  };

  const response =  await fetch(`http://localhost:8001/createInteraction/`, requestOptions)
  const body = await response.json();
  if(!response.ok){
    console.log(response.status)
    return Promise.reject(body);
  }
  else{
    console.log(response.status);
  }
}

async function fetchData(q,isThissearch,uritoload,q_iskey) {
  let base_url;
  let eventType;
  console.log(isThissearch,uritoload);
  if(!isThissearch){
     base_url =uritoload;
  }
  else
  {
    q=q.replace(/[\/\\]/g,'');
    if(!q_iskey){
    q = encodeURIComponent(q);
    base_url=`http://localhost:8001/search/${q}?format=json`
    }
    else{
      eventType="viewsimilar";
      postClickEvent(q,eventType);
      base_url=`http://localhost:8001/similardoc/${q}?format=json`
      // Update 'quality' for sm2
      const requestOptions2 = {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ quality: 3 })
      };
      fetch(`http://localhost:8001/rediscover/${q}/?format=json`, requestOptions2);

    }
  }
  const response = await fetch(base_url, {
    "method": "GET",
    });
  
  
  const body = await response.json();
  console.log(body);
  if(!isThissearch){
  return body;
}
else{
  return body;
}
}



function App() {
  const [query, setQuery] = React.useState("");
  const [list, setList] = React.useState([]);
  const [pagenum,setPagenum] =React.useState(1);
  const [nextpgelink,setNextpgelink] =React.useState("http://localhost:8001/feed?page=1&format=json")
  const [prevpgelink,setPrevpgelink] =React.useState("http://localhost:8001/feed?page=1&format=json")
  const [opensnackbar, setOpensnackbar] = React.useState(false);
  const [snackbartext, setSnackbartext] = React.useState("");
  
  const Alert = React.forwardRef(function Alert(props, ref) {
    return React.createElement(MuiAlert, Object.assign({ elevation: 6, ref: ref, variant: "filled" }, props));
  });

  const handleClosesnackbar = (event, reason) => {
    if (reason === "clickaway") {
        return;
    }
    setOpensnackbar(false);
  };

  

  const LoadFeed = (isThissearch=false,uritoload ="http://localhost:8001/feed?page=1&format=json",q_iskey=false,qq=undefined,updaterec=false) => {
    if(qq===undefined){
      qq=query
    }

    fetchData(qq,isThissearch,uritoload,q_iskey).then((newlist)=>{setList(list=>(newlist['results']===undefined)?newlist:newlist['results']);
    setNextpgelink(n=>(newlist['next']!==null && newlist['next']!==undefined && newlist['next'].includes('&updaterecom=1'))?newlist['next'].replace('&updaterecom=1',''):newlist['next']);
    setPrevpgelink(n=>newlist['previous']);
    setPagenum(n=>newlist['currentpage']);
    if(uritoload.includes("updaterecom=1")){
      setSnackbartext("Recommendations Updated");
      setOpensnackbar(true);
    }
    
  });
    window.scrollTo(0,0);
  };

 
  // This function updates the bookmarkflag into the database
  const handleChangeCheckbox = async (keyid,flag) =>{
    const requestOptions = {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ bookmarkflag: !flag })
    };
    const response = await fetch(`http://localhost:8001/feed/${keyid}/?format=json`, requestOptions)
    const body = await response.json();
    if(!response.ok){
      return Promise.reject(body);
    }
    else{
      console.log("changing toggle");
      postClickEvent(keyid,flag?"itemBookmarkToggledOff":"itemBookmarkToggledOn");
    setList(
      list.map(item => {
        if (item.keyid === keyid) {
          return { ...item, bookmarkflag: !item.bookmarkflag };
        } else {
          return item;
        }
      })
    );  

    }
  };


  // This function updates the views count of the item in the database
  const handleclicklink = async (keyid,view) =>{
    console.log("link clicked");
    const requestOptions = {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ views: (view+1) })
    };
    const requestOptions2 = {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ quality: 2 })
    };

    const response = await fetch(`http://localhost:8001/feed/${keyid}/?format=json`, requestOptions)
    const body = await response.json();
    if(!response.ok){
      return Promise.reject(body);
    }
    else{
      console.log("Item view updated");
      postClickEvent(keyid,"titlelinkclick");
      fetch(`http://localhost:8001/rediscover/${keyid}/?format=json`, requestOptions2);
      setList(
        list.map(item => {
          if (item.keyid === keyid) {
            return { ...item, views: item.views+1 };
          } else {
            return item;
          }
        })
      );
    }
  };

  const handleChangeRating = (val,keyid) => {
    // console.log("InhandlechangeRaring ",keyid,val);
    setList(
      list.map(item => {
        if (item.keyid === keyid) {
          return { ...item, rating: val};
        } else {
          return item;
        }
      })
    );
  };

// This function updates the rating of an item
  const handleAfterChange = async (val, keyid) => {
    console.log("handleAfterChange ",keyid,val);
    const requestOptions = {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ rating: val })
    };
    const response = await fetch(`http://localhost:8001/feed/${keyid}/?format=json`, requestOptions)
    const body = await response.json();
    if(!response.ok){
      return Promise.reject(body);
    }
    else{
      console.log("Item rating updated");
      let qult;
      if(val<0){
        qult=5;
      }
      else{
        qult=2;
      }
      const requestOptions2 = {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ quality: qult })
      };
      fetch(`http://localhost:8001/rediscover/${keyid}/?format=json`, requestOptions2);
      postClickEvent(keyid,`itemRatingchanged${val}`);
      setList(
        list.map(item => {
          if (item.keyid === keyid) {
            return { ...item, rating: val };
          } else {
            return item;
          }
        })
      );
    }
    console.log("AfterChange", keyid, val);
  };

  const onChangesnooze = async (keyid,val)=>{
    console.log(keyid,val);
    let ts = new Date(Date.now())
    // val=parseInt(val.substring(0, val.indexOf(' ')));
    const requestOptions = {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ snoozed_date: ts,
        snoozeval_days:val,snooze_priority:parseInt("-2") })
    };
    console.log(requestOptions);
    const response = await fetch(`http://localhost:8001/feed/${keyid}/?format=json`, requestOptions)
    const body = await response.json();
    if(!response.ok){
      return Promise.reject(body);
    }
    else{
      console.log("Item view updated");
      postClickEvent(keyid,`itemSnoozed${val}`);
      setSnackbartext(`Item snoozed for ${val} days`);
      setOpensnackbar(true);
      setList(
        list.filter((item) => item.keyid !== keyid)
      );
    }
  }
  
  React.useEffect(() => {
    let ignore = false;
    console.log("Loading page")
    if (!ignore) {
      LoadFeed();
    }
    return () => { ignore = true; }
    },[]);

    
  return (
    <div className="app">
      <div className="inner-container">
      <div className='profiledropdown'><RecipeReviewCard></RecipeReviewCard></div>
      <Button key = "loadfeedbutton" color="blue" name="Refresh Feed" onClick={(e)=>LoadFeed(false,'http://localhost:8001/feed?updaterecom=1&page=1&format=json')}/>
      </div>
       <form onSubmit={(e)=>(e.preventDefault(),LoadFeed(true))}> 
        <input
          autoFocus
          value={query}
          onChange={e => setQuery(e.target.value)}
        />
        <Button key="searchsubmitbutton" type='submit' color="green" name="Search" />
        {/* <button>Load</button> */}
      </form>
      {<FeedSelectFilter LoadFeed={LoadFeed}></FeedSelectFilter>}
      {!list
        ? null
        : list.length === 0
          ? <p><i>No results</i></p>
          : <ul>
            {list.map((item, index) => (
              <Item keyid={item.keyid} item={item} handleChangeCheckbox={handleChangeCheckbox} viewHandler={handleclicklink} handleAfterChange={handleAfterChange}
              handleChangeRating={handleChangeRating} LoadFeed={LoadFeed} onChangesnooze={onChangesnooze} setList={setList}
              setOpensnackbar={setOpensnackbar} setSnackbartext={setSnackbartext}/>
            ))}
          </ul>
      }
      <div className='rowC'>
       <Button key = "prevPage" color="red" name="<Previous" onClick={()=>LoadFeed(false,prevpgelink)}/>
       <h3>Page {pagenum}</h3>
      <Button key = "nextPage" color="green" name="Next>" onClick={()=>LoadFeed(false,nextpgelink)}/>
      </div>
      <Snackbar open={opensnackbar} autoHideDuration={2000} onClose={handleClosesnackbar}  anchorOrigin= {{horizontal: 'left',vertical: 'top'}} >
      <Alert onClose={handleClosesnackbar} severity="success" sx={{ width: "100%" }}>
        {snackbartext}
      </Alert>
    </Snackbar>
    </div>
    
  );
}




export default App;