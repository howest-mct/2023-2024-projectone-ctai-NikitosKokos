document.addEventListener('DOMContentLoaded', () => {
   const menuLinks = document.querySelectorAll('.sidebar__link');

   menuLinks.forEach(link => {
      link.addEventListener('click', (e) => {
         e.preventDefault();
         menuLinks.forEach(el => {
            el.classList.remove('_active');
         });
         link.classList.add('_active');
      });
   })

   const inputs = document.querySelectorAll('.input-anim');

   if(inputs.length > 0){
      const handleFocusIn = (e) => {
         const input = e.target;
         const label = input.nextElementSibling;
         label.classList.add('focus');
         setTimeout(() => {
            input.classList.add('blink');
         }, 300);

      }

      const handleFocusOut = (e) => {
         const input = e.target;
         const label = input.nextElementSibling;
         if(input.value === ''){
            label.classList.remove('focus');
            input.classList.remove('blink');
         }
      }

      const initInput = (input) => {
         const placeholder = input.placeholder
         input.placeholder = '';
         const label = input.nextElementSibling;
         label.textContent = placeholder;
      }

      inputs.forEach(input => {
         initInput(input);

         
         const inputField = input.closest('.form-main__input');
         const passwordBtn = inputField.querySelector('.form-main__eye');

         if(passwordBtn){
            passwordBtn.addEventListener('click', () => {
               inputField.classList.toggle('show');
               if(input.type === 'password'){
                  input.type = 'text';
               }else{
                  input.type = 'password';
               }
            });
         }

         input.addEventListener('focusin', handleFocusIn);
         input.addEventListener('focusout', handleFocusOut);
      });
   }

   // * form
   const signupForm = document.querySelector('.form-main');
   let inputName, inputLastName, inputPassword;
   if(signupForm){
      inputName = signupForm.userFirstName
      inputLastName = signupForm.userLastName
      inputPassword = signupForm.userPassword
   }
         
   // * buttons
   const buttons = document.querySelectorAll('.btn');
   if(buttons.length > 0){
      const isInputsHaveFocus = e => {
         let isUnFocus = false; 
         if(e.offsetX === 0 && e.offsetY === 0){
            isUnFocus = true;
         }else if(signupForm){
            if(document.activeElement === inputName || document.activeElement === inputLastName || document.activeElement === inputPassword){
               isUnFocus = true;
            }
         }else if(e.pointerId === -1){
            isUnFocus = true;
         }
         return isUnFocus;
      }
      buttons.forEach(btn => {
         btn.addEventListener('click', e => {
            let x = e.offsetX;
            let y = e.offsetY;
            if(isInputsHaveFocus(e)){
               x = e.target.offsetWidth / 2;
               y = e.target.offsetHeight / 2;
            }

            const size = Math.max(e.target.offsetWidth, e.target.offsetHeight) * 2;

            const ripples = document.createElement('span');
            ripples.style.left = `${x}px`;
            ripples.style.top = `${y}px`;
            setTimeout(() => {
               ripples.style.width = `${size}px`;
               ripples.style.height = `${size}px`;            
               ripples.style.opacity = '0';            
            }, 5);
            btn.appendChild(ripples);
            setTimeout(() => {
               ripples.remove();
            }, 500);
         });
      })      
   }

   // * tabs
   const tabs = document.querySelectorAll('.users__tab');

   if(tabs.length > 0){
      const empty = document.querySelector('.users__empty');
      const isEmpty = empty.classList.contains('_show');
      const popup = document.querySelector('.users__popup');

      if(popup){
         setTimeout(() => {
            popup.classList.add('show');
         }, 0);

         setTimeout(() => {
            popup.classList.remove('show');
         }, 5000);
      }


      tabs.forEach(tab => {
         tab.addEventListener('click', () => {
            tab.classList.toggle('_active');
            updateFilters();
         });
      });


      const filters = gsap.utils.toArray('.users__tab'),
         items = gsap.utils.toArray('.users__item');

      function updateFilters() {
      const state = Flip.getState(items), // get the current state
            classes = filters.filter(checkbox => checkbox.classList.contains('_active')).map(checkbox => "." + checkbox.textContent),
            matches = classes.length ? gsap.utils.toArray(classes.join(",")) : classes;

      // adjust the display property of each item ("none" for filtered ones, "inline-flex" for matching ones)
      items.forEach(item => item.style.display = matches.indexOf(item) === -1 ? "none" : "inline-flex");

      const value = Array.from(items).reduce((acc, el) => (matches.indexOf(el) === -1 ? acc : acc+1), 0);
      
      if(!value && !empty.classList.contains('_show')){
         empty.classList.add('_show');
      }else if(!isEmpty){
         empty.classList.remove('_show');
      }
      
      // animate from the previous state
         Flip.from(state, {
            duration: .6,
         scale: true,
         // absolute: true,
         ease: "power1.inOut",
            onEnter: elements => gsap.fromTo(elements, {opacity: 0, scale: 0}, {opacity: 1, scale: 1, duration: .6}),
            onLeave: elements => gsap.to(elements, {opacity: 0, scale: 0, duration: .6})
         }); 
      }      
   }

   // * record

   const recordBtn = document.querySelector('.record__btn');

   if(recordBtn){
      const icon1 = document.querySelector('.record__icon img');
      const icon2 = document.querySelector('.record__icon img._hide');
      const title = document.querySelector('.record__title');
      const record = document.querySelector('.record');
      const progress = document.querySelector('.progress');
      const steps = Array.from(document.querySelectorAll('.progress__step'));

      const makeDataset = () => {
         record.classList.add('_hide');
         progress.classList.remove('_hide');

         fetch('/split', {
            method: 'POST',
            headers: {
               'Content-Type': 'application/json'
           },
            body: JSON.stringify({ className: recordBtn.dataset.id })
        })
        .then(response => {
            if (!response.ok) {
               throw new Error('Failed to start detection task');
            }
            return response.json();
        })
        .then(data => {
            console.log(data.message); // Log the message from the server
            if(data.message === 'Ok'){
               trainModel();
            }
         })
        .catch(error => console.error(error));  // Handle errors
      }

      const trainModel = () => {
         steps[0].classList.remove('_progress');
         steps[0].classList.add('_done');
         steps[1].classList.add('_progress');

         fetch('/train', {
            method: 'GET',
            headers: {
               'Content-Type': 'application/json'
           }
        })
        .then(response => {
            if (!response.ok) {
               throw new Error('Failed to start detection task');
            }
            return response.json();
        })
        .then(data => {
            if(data.message === 'Ok'){
               chooseTheBest();
            }
         })
        .catch(error => console.error(error));  // Handle errors
      }

      const chooseTheBest = () => {
         steps[1].classList.remove('_progress');
         steps[1].classList.add('_done');
         steps[2].classList.add('_progress');

         fetch('/best', {
            method: 'POST',
            headers: {
               'Content-Type': 'application/json'
           },
            body: JSON.stringify({ userId: recordBtn.dataset.id })
        })
        .then(response => {
            if (response.status === 200) {
               return response.json();
            } else if (response.status === 302) {
                  // Handle redirection manually
                  window.location.href = response.url;
            } else {
                  throw new Error('Failed to start detection task');
            }
        }) 
        .then(data => {
            if (data.redirect_url) {
               window.location.href = data.redirect_url;
            } else {
               console.log(data.message);
            }
         })
        .catch(error => console.error(error));  // Handle errors
      }

      recordBtn.addEventListener('click', () => {
         icon1.classList.add('_hide');
         icon2.classList.remove('_hide');
         recordBtn.textContent = 'Recording...';
         recordBtn.disabled = true;
         title.textContent = 'Move your head a bit';

         fetch('/recording', {
            method: 'POST',
            headers: {
               'Content-Type': 'application/json'
           },
            body: JSON.stringify({ userId: recordBtn.dataset.id })
        })
        .then(response => {
            if (!response.ok) {
               throw new Error('Failed to start detection task');
            }
            return response.json();
        }) 
        .then(data => {
         if(data.message === 'Ok'){
            makeDataset();
         }
     })
        .catch(error => console.error(error));  // Handle errors
      });
   }


   // * auth
   const auth = document.querySelector('.auth');
   if(auth){
      document.body.style.backgroundColor = "#F2709C";
      setTimeout(() => {
         auth.classList.add('_lock');
         document.body.style.transition = 'background-color .3s cubic-bezier(0.34, 1.55, 0.64, 1)';
      }, 200);
   
      const loggedIn = () => {
         auth.classList.add('_open');
         document.body.style.backgroundColor = "#fff";
      }

      const errorLoggedIn = () => {
         auth.classList.add('_error');
      }

      // const setAnimation = () => {
      //    const value = 1.55;
      //    const w = window.innerWidth;
      //    const h = window.innerHeight;
      //    const wValue = value * (((w - 1920) * -0.001) + 1)
      // }

      // window.addEventListener('resize', setAnimation);
      // setAnimation();

      // const authCont = document.querySelector('.auth__open');
      // const getMinValues = () => {
      //    let minW = authCont.offsetWidth; // 33.75
      //    let minH = authCont.offsetHeight; // 66.66...
      //    setInterval(() => {
      //       if(minW > authCont.offsetWidth){
      //          minW = authCont.offsetWidth
      //       }
      //       if(minH > authCont.offsetHeight){
      //          minH = authCont.offsetHeight
      //       }
      //    }, 1);
      //    setTimeout(() => {
      //       console.log('minW',minW/authCont.offsetWidth * 100);
      //       console.log('minH',minH/authCont.offsetHeight * 100);
      //    }, 2000);
      // }

      // getMinValues();

      fetch('/auth', {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json'
        },
         body: JSON.stringify({ userId: auth.dataset.id })
     })
     .then(response => {
         if (!response.ok) {
            throw new Error('Failed to start detection task');
         }
         return response.json();
     })
     .then(data => {
         if(data.message === 'Ok'){
            loggedIn();
         }else{
            errorLoggedIn();
         }
      })
     .catch(error => console.error(error));
   }

}); // end;
// webp support
function testWebP(callback) {
  let webP = new Image();
  webP.onload = webP.onerror = function () {
    callback(webP.height == 2);
  };
  webP.src =
    "data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA";
}
//=================
testWebP(function (support) {
  if (support == true) {
    document.querySelector("body").classList.add("webp");
  } else {
    document.querySelector("body").classList.add("no-webp");
  }
});;
/**
 * data-state="active" make open current select
 * data-default set deafault value before initialization
 */

const selectSingle = document.querySelectorAll('[data-state]');
const selectSingle_title = document.querySelectorAll('[data-default]');
const labels = document.querySelectorAll('[data-for]');

if (selectSingle) {

   const hideMenu = (element) => {
      element.setAttribute('data-state', '');
      element.querySelector('.select__title').classList.remove('active');
   }
   const showMenu = (element) => {
      selectSingle.forEach(el => {
         el.setAttribute('data-state', '');
         el.querySelector('.select__title').classList.remove('active');
      })
      element.setAttribute('data-state', 'active');
      element.querySelector('.select__title').classList.add('active');
   }

   // Toggle menu
   const toggleMenu = (element) => {
      if ('active' === element.getAttribute('data-state')){
         hideMenu(element);
      } else {
         showMenu(element);
      }
   }

   labels.forEach(label => {
      label.addEventListener('click', () => {
         const dataFor = label.getAttribute('data-for');
         const element = document.querySelector(`[data-name="${dataFor}"]`);
         toggleMenu(element);
      });
   })
   selectSingle.forEach((element, index) => {
      if(element.dataset.name === 'honorific'){
         element.closest('.form-main__select').style.display = "none";
      }

      const title = selectSingle_title[index];

      title.querySelector('span').innerHTML = title.dataset.default;

      document.addEventListener('click', documentActions);

      function documentActions(e) {
      const targetEl = e.target;
   
         if(!targetEl.closest('[data-state]') && !targetEl.closest('[data-for]')){
            element.setAttribute('data-state', '');
            element.querySelector('.select__title').classList.remove('active');
         }
      }

      element.addEventListener('keydown', (e) => {
         if (e.key === 'Enter'){
            toggleMenu(element);
         }
         if(e.key === 'Tab'){
            hideMenu(element);
         }
      });

      title.addEventListener('click', () => toggleMenu(element));

      element.querySelector('.select__body').addEventListener('click', (e) => {
         const targetEl = e.target;
         if(targetEl.closest('input')){
            selectSingle_title[index].querySelector('span').textContent = targetEl.value;
            element.setAttribute('data-state', '');
            
            if(targetEl.value === 'Teacher'){
               element.closest('.form-main__select').nextElementSibling.style.display = "block";
            }else if(targetEl.value === 'Student'){
               element.closest('.form-main__select').nextElementSibling.style.display = "none";
               const honorific = element.closest('.form-main__select').nextElementSibling.querySelector('[data-state]');

               const title = honorific.querySelector('[data-default]');

               title.querySelector('span').innerHTML = title.dataset.default;

               honorific.querySelectorAll('input').forEach(input => {
                  input.checked = false;
               });
            }
         }
      })
      // let selectSingle_labels = element.querySelectorAll('label');
      // // Close when click to option
      // for (let i = 0; i < selectSingle_labels.length; i++) {
      //    selectSingle_labels[i].addEventListener('click', (evt) => {
      //       selectSingle_title[index].textContent = evt.target.textContent;
      //       element.setAttribute('data-state', '');
      //    });
      // }
   });
};