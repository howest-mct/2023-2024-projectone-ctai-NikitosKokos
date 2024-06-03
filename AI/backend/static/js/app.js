// @ @include('files/regular.js', {});
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

   const auth = document.querySelector('.auth');
   if(auth){
      document.body.style.backgroundColor = "#F2709C";
      setTimeout(() => {
         auth.classList.add('_lock');
         document.body.style.transition = 'background-color .3s cubic-bezier(0.34, 1.55, 0.64, 1)';
      }, 200);
   
      // setTimeout(() => {
      //    auth.classList.add('_open');
      //    document.body.style.backgroundColor = "#fff";
      // }, 2200);
      const pressEnter = (e) => {
         if(e.code == 'Space'){
            auth.classList.add('_open');
            document.body.style.backgroundColor = "#fff";
         }
      }
      document.addEventListener("keydown", pressEnter);
   

      const setAnimation = () => {
         // --anim: cubic-bezier(0.34, 1.55, 0.64, 1);
         const value = 1.55;
         const w = window.innerWidth;
         const h = window.innerHeight;
         const wValue = value * (((w - 1920) * -0.001) + 1)
         // console.log(wValue);
         // auth.style.setProperty('--anim', `cubic-bezier(0.34, ${wValue}, 0.64, 1)`);
      }

      window.addEventListener('resize', setAnimation);
      setAnimation();

      const authCont = document.querySelector('.auth__open');
      const getMinValues = () => {
         let minW = authCont.offsetWidth; // 33.75
         let minH = authCont.offsetHeight; // 66.66...
         setInterval(() => {
            if(minW > authCont.offsetWidth){
               minW = authCont.offsetWidth
            }
            if(minH > authCont.offsetHeight){
               minH = authCont.offsetHeight
            }
         }, 1);
         setTimeout(() => {
            console.log('minW',minW/authCont.offsetWidth * 100);
            console.log('minH',minH/authCont.offsetHeight * 100);
         }, 2000);
      }

      getMinValues();
   }

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
            // const value = Array.from(tabs).reduce((acc, el) => (el.classList.contains('_active') ? acc+1 : acc), 0);
            // if(!value && !empty.classList.contains('_show')){
            //    empty.classList.add('_show');
            // }else if(!isEmpty){
            //    empty.classList.remove('_show');
            // }
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


   
}); // end;
// @ @include('files/forms.js', {});
// поддержка webp
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
});
//=================
// da (class,place,breakpoint)
("use strict");

(function () {
  let originalPositions = [];
  let daElements = document.querySelectorAll("[data-da]");
  let daElementsArray = [];
  let daMatchMedia = [];
  //Заполняем массивы
  if (daElements.length > 0) {
    let number = 0;
    for (let index = 0; index < daElements.length; index++) {
      const daElement = daElements[index];
      const daMove = daElement.getAttribute("data-da");
      if (daMove != "") {
        const daArray = daMove.split(",");
        const daPlace = daArray[1] ? daArray[1].trim() : "last";
        const daBreakpoint = daArray[2] ? daArray[2].trim() : "767";
        const daType = daArray[3] === "min" ? daArray[3].trim() : "max";
        const daDestination = document.querySelector("." + daArray[0].trim());
        if (daArray.length > 0 && daDestination) {
          daElement.setAttribute("data-da-index", number);
          //Заполняем массив первоначальных позиций
          originalPositions[number] = {
            parent: daElement.parentNode,
            index: indexInParent(daElement),
          };
          //Заполняем массив элементов
          daElementsArray[number] = {
            element: daElement,
            destination: document.querySelector("." + daArray[0].trim()),
            place: daPlace,
            breakpoint: daBreakpoint,
            type: daType,
          };
          number++;
        }
      }
    }
    dynamicAdaptSort(daElementsArray);

    //Создаем события в точке брейкпоинта
    for (let index = 0; index < daElementsArray.length; index++) {
      const el = daElementsArray[index];
      const daBreakpoint = el.breakpoint;
      const daType = el.type;

      daMatchMedia.push(
        window.matchMedia("(" + daType + "-width: " + daBreakpoint + "px)")
      );
      daMatchMedia[index].addListener(dynamicAdapt);
    }
  }
  //Основная функция
  function dynamicAdapt(e) {
    for (let index = 0; index < daElementsArray.length; index++) {
      const el = daElementsArray[index];
      const daElement = el.element;
      const daDestination = el.destination;
      const daPlace = el.place;
      const daBreakpoint = el.breakpoint;
      const daClassname = "_dynamic_adapt_" + daBreakpoint;

      if (daMatchMedia[index].matches) {
        //Перебрасываем элементы
        if (!daElement.classList.contains(daClassname)) {
          let actualIndex = indexOfElements(daDestination)[daPlace];
          if (daPlace === "first") {
            actualIndex = indexOfElements(daDestination)[0];
          } else if (daPlace === "last") {
            actualIndex = indexOfElements(daDestination)[
              indexOfElements(daDestination).length
            ];
          }
          daDestination.insertBefore(
            daElement,
            daDestination.children[actualIndex]
          );
          daElement.classList.add(daClassname);
        }
      } else {
        //Возвращаем на место
        if (daElement.classList.contains(daClassname)) {
          dynamicAdaptBack(daElement);
          daElement.classList.remove(daClassname);
        }
      }
    }
    customAdapt();
  }

  //Вызов основной функции
  dynamicAdapt();

  //Функция возврата на место
  function dynamicAdaptBack(el) {
    const daIndex = el.getAttribute("data-da-index");
    const originalPlace = originalPositions[daIndex];
    const parentPlace = originalPlace["parent"];
    const indexPlace = originalPlace["index"];
    const actualIndex = indexOfElements(parentPlace, true)[indexPlace];
    parentPlace.insertBefore(el, parentPlace.children[actualIndex]);
  }
  //Функция получения индекса внутри родителя
  function indexInParent(el) {
    var children = Array.prototype.slice.call(el.parentNode.children);
    return children.indexOf(el);
  }
  //Функция получения массива индексов элементов внутри родителя
  function indexOfElements(parent, back) {
    const children = parent.children;
    const childrenArray = [];
    for (let i = 0; i < children.length; i++) {
      const childrenElement = children[i];
      if (back) {
        childrenArray.push(i);
      } else {
        //Исключая перенесенный элемент
        if (childrenElement.getAttribute("data-da") == null) {
          childrenArray.push(i);
        }
      }
    }
    return childrenArray;
  }
  //Сортировка объекта
  function dynamicAdaptSort(arr) {
    arr.sort(function (a, b) {
      if (a.breakpoint > b.breakpoint) {
        return -1;
      } else {
        return 1;
      }
    });
    arr.sort(function (a, b) {
      if (a.place > b.place) {
        return 1;
      } else {
        return -1;
      }
    });
  }
  //Дополнительные сценарии адаптации
  function customAdapt() {
    //const viewport_width = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
  }
})();
//=================
// ibg
function ibg() {
  let ibg = document.querySelectorAll("._ibg");
  for (var i = 0; i < ibg.length; i++) {
    if (ibg[i].querySelector("img")) {
      ibg[i].style.backgroundImage =
        "url(" + ibg[i].querySelector("img").getAttribute("src") + ")";
    }
  }
}

let observer = new MutationObserver((mutationRecords) => {
  mutationRecords.forEach(item => {
    if(item.addedNodes[0]){
      if(item.addedNodes[0].classList){
        if(item.addedNodes[0].classList.contains('_ibg')) ibg()
      }
    }
  });
});

observer.observe(document.body, {
  childList: true,
  subtree: true,
});

ibg();
//=================
// isMobile
const isMobile = { Android: function () { return navigator.userAgent.match(/Android/i); }, BlackBerry: function () { return navigator.userAgent.match(/BlackBerry/i); }, iOS: function () { return navigator.userAgent.match(/iPhone|iPad|iPod/i); }, Opera: function () { return navigator.userAgent.match(/Opera Mini/i); }, Windows: function () { return navigator.userAgent.match(/IEMobile/i); }, any: function () { return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows()); } };
//=================
//RemoveClasses
function _removeClasses(el, class_name) {
	for (let i = 0; i < el.length; i++) {
		el[i].classList.remove(class_name);
	}
}
//=================
//SlideToggle
let _slideUp = (target, duration = 500) => {
	target.style.transitionProperty = 'height, margin, padding';
	target.style.transitionDuration = duration + 'ms';
	target.style.height = target.offsetHeight + 'px';
	target.offsetHeight;
	target.style.overflow = 'hidden';
	target.style.height = 0;
	target.style.paddingTop = 0;
	target.style.paddingBottom = 0;
	target.style.marginTop = 0;
	target.style.marginBottom = 0;
	window.setTimeout(() => {
		target.style.display = 'none';
		target.style.removeProperty('height');
		target.style.removeProperty('padding-top');
		target.style.removeProperty('padding-bottom');
		target.style.removeProperty('margin-top');
		target.style.removeProperty('margin-bottom');
		target.style.removeProperty('overflow');
		target.style.removeProperty('transition-duration');
		target.style.removeProperty('transition-property');
		target.classList.remove('_slide');
	}, duration);
}
let _slideDown = (target, duration = 500) => {
	target.style.removeProperty('display');
	let display = window.getComputedStyle(target).display;
	if (display === 'none')
		display = 'block';

	target.style.display = display;
	let height = target.offsetHeight;
	target.style.overflow = 'hidden';
	target.style.height = 0;
	target.style.paddingTop = 0;
	target.style.paddingBottom = 0;
	target.style.marginTop = 0;
	target.style.marginBottom = 0;
	target.offsetHeight;
	target.style.transitionProperty = "height, margin, padding";
	target.style.transitionDuration = duration + 'ms';
	target.style.height = height + 'px';
	target.style.removeProperty('padding-top');
	target.style.removeProperty('padding-bottom');
	target.style.removeProperty('margin-top');
	target.style.removeProperty('margin-bottom');
	window.setTimeout(() => {
		target.style.removeProperty('height');
		target.style.removeProperty('overflow');
		target.style.removeProperty('transition-duration');
		target.style.removeProperty('transition-property');
		target.classList.remove('_slide');
	}, duration);
}
let _slideToggle = (target, duration = 500) => {
	if (!target.classList.contains('_slide')) {
		target.classList.add('_slide');
		if (window.getComputedStyle(target).display === 'none') {
			return _slideDown(target, duration);
		} else {
			return _slideUp(target, duration);
		}
	}
}
//=================
//IsHidden
function _is_hidden(el) {
	return (el.offsetParent === null)
}
//=================
let unlock = true;
let popups = document.querySelectorAll('.popup');

for (let index = 0; index < popups.length; index++) {
	const popup = popups[index];
	popup.addEventListener("click", function (e) {
		if (!e.target.closest('.popup__body')) {
			popup_close(e.target.closest('.popup'));
		}
	});
}
//=================
function popup_open(item, video = '') {
	let activePopup = document.querySelectorAll('.popup._active');
	if (activePopup.length > 0) {
		popup_close('', false);
	}
	let curent_popup = document.querySelector('.popup_' + item);
	if (curent_popup && unlock) {
		if (video != '' && video != null) {
			let popup_video = document.querySelector('.popup_video');
			popup_video.querySelector('.popup__video').innerHTML = '<iframe src="https://www.youtube.com/embed/' + video + '?autoplay=1"  allow="autoplay; encrypted-media" allowfullscreen></iframe>';
		}
		if (!document.querySelector('.menu__body._active')) {
			body_lock_add(500);
		}
		curent_popup.classList.add('_active');
		history.pushState('', '', '#' + item);
	}
}
//=================
function popup_close(item, bodyUnlock = true) {
	if (unlock) {
		if (!item) {
			for (let index = 0; index < popups.length; index++) {
				const popup = popups[index];
				let video = popup.querySelector('.popup__video');
				if (video) {
					video.innerHTML = '';
				}
				popup.classList.remove('_active');
			}
		} else {
			let video = item.querySelector('.popup__video');
			if (video) {
				video.innerHTML = '';
			}
			item.classList.remove('_active');
		}
		if (!document.querySelector('.menu__body._active') && bodyUnlock) {
			body_lock_remove(500);
		}
		history.pushState('', '', window.location.href.split('#')[0]);
	}
}
//=================
let popup_close_icon = document.querySelectorAll('.popup__close,._popup-close');
if (popup_close_icon) {
	for (let index = 0; index < popup_close_icon.length; index++) {
		const el = popup_close_icon[index];
		el.addEventListener('click', function () {
			popup_close(el.closest('.popup'));
		})
	}
}
document.addEventListener('keydown', function (e) {
	if (e.key  == 'Escape') {
		popup_close();
	}
});
//=================
// body lock
function body_lock(delay) {
	let body = document.querySelector("body");
	if (body.classList.contains('_lock')) {
		body_lock_remove(delay);
	} else {
		body_lock_add(delay);
	}
}
function body_lock_remove(delay) {
	let body = document.querySelector("body");
	if (unlock) {
		let lock_padding = document.querySelectorAll("._lp");
		setTimeout(() => {
			for (let index = 0; index < lock_padding.length; index++) {
				const el = lock_padding[index];
				el.style.paddingRight = '0px';
			}
			body.style.paddingRight = '0px';
			body.classList.remove("_lock");
		}, delay);

		unlock = false;
		setTimeout(function () {
			unlock = true;
		}, delay);
	}
}

function body_lock_add(delay) {
	let body = document.querySelector("body");
	if (unlock) {
		let lock_padding = document.querySelectorAll("._lp");
		for (let index = 0; index < lock_padding.length; index++) {
			const el = lock_padding[index];
			el.style.paddingRight = window.innerWidth - document.querySelector('.wrapper').offsetWidth + 'px';
		}
		body.style.paddingRight = window.innerWidth - document.querySelector('.wrapper').offsetWidth + 'px';
		body.classList.add("_lock");

		unlock = false;
		setTimeout(function () {
			unlock = true;
		}, delay);
	}
}
//=================
//Gallery
let gallery = document.querySelectorAll('._gallery');
if (gallery) {
	gallery_init();
}
function gallery_init() {
	for (let index = 0; index < gallery.length; index++) {
		const el = gallery[index];
		lightGallery(el, {
			counter: false,
			selector: 'a',
			download: false
		});
	}
}
//=================;
// @ @include('files/burger.js', {});
// @ @include("files/spoller.js",{});
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
// @ @include("files/tabs.js",{});
// @ @include("files/sliders.js",{});