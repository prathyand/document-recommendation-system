import * as React from "react";
import Button from "@mui/material/Button";
import ClickAwayListener from "@mui/material/ClickAwayListener";
import Grow from "@mui/material/Grow";
import Paper from "@mui/material/Paper";
import Popper from "@mui/material/Popper";
import MenuItem from "@mui/material/MenuItem";
import MenuList from "@mui/material/MenuList";
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive';

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
// import CheckIcon from '@mui/icons-material/Check';
// import CheckCircleIcon from '@mui/icons-material/CheckCircle';


export default function MenuListComposition(props) {
    const [open, setOpen] = React.useState(false);
    const anchorRef = React.useRef(null);
    const handleToggle = () => {
        setOpen((prevOpen) => !prevOpen);
    };


    const handleClose = (event) => {
        
        if (anchorRef.current &&
            anchorRef.current.contains(event.target)) {
            return;
        }
        
        setOpen(false);
    };

    const onChangesnooze = async (event)=>{
        console.log(props.keyid,event.target.id);
        var idmap = {
            "1": 2,
            '2': 7,
            '3':14
          };
          let ts = '1000-01-01T00:00:00Z';
          let val = -1;
          let sp =-1;
        if(event.target.id!=='0'){
            ts = new Date(Date.now());
            val = idmap[event.target.id];
            sp =-2;
        }
        const requestOptions = {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ snoozed_date: ts,
            snoozeval_days:val,snooze_priority:sp })
        };
        console.log(requestOptions);
        const response = await fetch(`http://localhost:8001/feed/${props.keyid}/?format=json`, requestOptions)
        const body = await response.json();
        if(!response.ok){
          return Promise.reject(body);
        }
        else{
          
          if(event.target.id==='0'){
            postClickEvent(props.keyid,"snoozeDismissed");
            props.setSnackbartext("Reminder Dismissed!");
          }
          else{
            postClickEvent(props.keyid,`itemSnoozed${val}`);
            props.setSnackbartext("Reminder Updated!");
          }
          console.log("updated !!");
          props.setOpensnackbar(true);
          setOpen(false);
          props.setList(list=>
              (list.filter((item) => item.keyid !== props.keyid))
            );
        }
      }

    function handleListKeyDown(event) {
        if (event.key === "Tab") {
            event.preventDefault();
            setOpen(false);
        }
        else if (event.key === "Escape") {
            setOpen(false);
        }
    }
    // return focus to the button when we transitioned from !open -> open
    const prevOpen = React.useRef(open);
    React.useEffect(() => {
        if (prevOpen.current === true && open === false) {
            anchorRef.current.focus();
        }
        prevOpen.current = open;
    }, [open]);
    return (React.createElement("div", null,
        React.createElement(Button, { ref: anchorRef, id: "composition-button", "aria-controls": open ? "composition-menu" : undefined, 
        "aria-expanded": open ? "true" : undefined, "aria-haspopup": "true", onClick: handleToggle, color: "success",variant:"outlined",
        startIcon:<NotificationsActiveIcon /> }, "Reminder"),
        React.createElement(Popper, { open: open, anchorEl: anchorRef.current, role: undefined, placement: "bottom-start", transition: true, disablePortal: true }, ({ TransitionProps, placement }) => (React.createElement(Grow, Object.assign({}, TransitionProps, { style: {
                transformOrigin: placement === "bottom-start" ? "left top" : "left bottom"
            } }),
            React.createElement(Paper, null,
                React.createElement(ClickAwayListener, { onClickAway: handleClose },
                    React.createElement(MenuList, { autoFocusItem: open, id: "composition-menu", "aria-labelledby": "composition-button", onKeyDown: handleListKeyDown },
                        React.createElement(MenuItem, { onClick: onChangesnooze,id:'0' }, "Dismiss"),
                        React.createElement(MenuItem, { onClick: onChangesnooze,id:'1' }, "Remind me in 2 days"),
                        React.createElement(MenuItem, { onClick: onChangesnooze,id:'2' }, "Remind me in 7 days"),
                        React.createElement(MenuItem, { onClick: onChangesnooze,id:'3' }, "Remind me in 14 days")))))))
                     
                        )
                        );
}