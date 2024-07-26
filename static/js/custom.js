/*
 *
 *		CUSTOM.JS
 *
 */

(function($){
	
	"use strict";
	
	// DETECT TOUCH DEVICE //
	function is_touch_device() {
		return !!('ontouchstart' in window) || ( !! ('onmsgesturechange' in window) && !! window.navigator.maxTouchPoints);
	}
	
	
	// PAGE LOADER //
	function page_loader() {	
		
		var hash = window.location.hash;
		
		$(".loader-img").delay(500).fadeOut();
		$("#page-loader").delay(1000).fadeOut("slow");
		
		if(!hash) {
			
		} else {
			$(document).scrollTop( $(hash).offset().top -56); 
		}
	}
	
	
	// SHOW/HIDE MOBILE MENU //
	function show_hide_mobile_menu() {
		
		$("#mobile-menu-button").on("click", function(e) {
            
			e.preventDefault();
			
			$("#mobile-menu").slideToggle(300);
			
        });	
		
	}
	
	
	// MOBILE MENU //
	function mobile_menu() {
		
		if ($(window).width() < 992) {
			
			if ($("#menu").length > 0) {
			
				if ($("#mobile-menu").length < 1) {
					
					$("#menu").clone().attr({
						id: "mobile-menu",
						class: ""
					}).insertAfter("#header");
					
					$("#mobile-menu .megamenu > a").on("click", function(e) {
                        
						e.preventDefault();
						
						$(this).toggleClass("open").next("div").slideToggle(300);
						
                    });
					
					$("#mobile-menu .dropdown > a").on("click", function(e) {
                        
						e.preventDefault();
						
						$(this).toggleClass("open").next("ul").slideToggle(300);
						
                    });
				
				}
				
			}
				
		} else {
			
			$("#mobile-menu").hide();
			
		}
		
	}
	
	
	// HEADER SEARCH //
	function header_search() {	
		
		$(".menu li.search a").on("click", function(e) { 
		
			e.preventDefault();
			
			if(!$(".menu li.search a").hasClass("open")) {
			
				$("#search-form").fadeIn().addClass("open");
				
				$("#search-form").append('<a class="close" href="#">x</a>');
				
			}
			
			$("#search-form a.close").on("click", function(e) { 
		
				e.preventDefault();
				$("#search-form").fadeOut().removeClass("open");
				$(this).remove();
				
			});
			
		});
		
		$(window).scroll(function(){

			$("#search-form").fadeOut(300);

		});
		
	}
	
	
	// STICKY //
	function sticky() {
		
		var sticky_point = $("#header-container").innerHeight() + 100;
		
		$("#header").clone().attr({
			id: "header-sticky",
			class: ""
		}).insertAfter("header");
		
		$(window).scroll(function(){
			
			if ($(window).scrollTop() > sticky_point) {  
				$("#header-sticky").slideDown(300).addClass("header-sticky");
				$("#header .menu ul, #header .menu .megamenu-container").css({"visibility": "hidden"});
			} else {
				$("#header-sticky").slideUp(100).removeClass("header-sticky");
				$("#header .menu ul, #header .menu .megamenu-container").css({"visibility": "visible"});
			}
			
		});
		
		$("#header-sticky .menu li.search a").on("click", function(e) { 
		
			e.preventDefault();
			
			if(!$("#header-sticky .menu li.search a").hasClass("open")) {
			
				$("#header-sticky #search-form").fadeIn().addClass("open");
				
				$("#header-sticky #search-form").append('<a class="close" href="#">x</a>');
				
			}
			
			$("#search-form a.close").on("click", function(e) { 
		
				e.preventDefault();
				$("#header-sticky #search-form").fadeOut().removeClass("open");
				$(this).remove();
				
			});
			
		});
		
		$(window).scroll(function(){

			$("#header-sticky #search-form").fadeOut(300);

		});
		
	}
	
	
	// FOOTER PARALLAX //
	function footer_parallax() {
		
		if ($(window).width() > 767 ) {
			$("#main-container").css("margin-bottom", $("#footer-container").height());
		}
		
	}
	
 
	// PROGRESS BARS // 
	function progress_bars() {
		
		$(".progress .progress-bar:in-viewport").each(function() {
			
			if (!$(this).hasClass("animated")) {
				$(this).addClass("animated");
				$(this).animate({
					width: $(this).attr("data-width") + "%"
				}, 2000);
			}
			
		});
		
	}


	// CHARTS //
	function pie_chart() {
		
		if (typeof $.fn.easyPieChart !== 'undefined') {
		
			$(".pie-chart:in-viewport").each(function() {
				
				$(this).easyPieChart({
					animate: 1500,
					lineCap: "square",
					lineWidth: $(this).attr("data-line-width"),
					size: $(this).attr("data-size"),
					barColor: $(this).attr("data-bar-color"),
					trackColor: $(this).attr("data-track-color"),
					scaleColor: "transparent",
					onStep: function(from, to, percent) {
						$(this.el).find(".pie-chart-percent .value").text(Math.round(percent));
					}
				});
				
			});
			
		}
		
	}
	
	// COUNTER //
	function counter() {
		
		if (typeof $.fn.jQuerySimpleCounter !== 'undefined') {
		
			$(".counter .counter-value:in-viewport").each(function() {
				
				if (!$(this).hasClass("animated")) {
					$(this).addClass("animated");
					$(this).jQuerySimpleCounter({
						start: 0,
						end: $(this).attr("data-value"),
						duration: 2000
					});	
				}
			
			});
			
		}
	}
	
	
	// STATISTICS //
	function statistics() {
		
		if (typeof Chart !== 'undefined') {
		
			$(".statistics-container .animate-chart:in-viewport").each(function() {
				
				if(!$(this).hasClass("animated")) {
					
					$(this).addClass("animated");
					
					// LINE CHART //
					var data1 = {
						labels : ["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100", "150", "200", "250", "300"],
						datasets : [
							{
								fill: "true",
								label: "Profit",
								backgroundColor: "transparent",
								borderWidth: 1,
								borderColor: "#72d3d5",
								pointBorderColor: "#72d3d5",
								pointBackgroundColor: "#fff",
								pointHoverBackgroundColor: "#fff",
								pointHoverBorderColor: "#72d3d5",
								pointBorderWidth: 1,
								pointHoverBorderWidth: 1,
								tension: 0,
								stacked: false,
								data : ["35", "25", "40", "35", "50", "45", "65", "70", "85", "75", "70", "73", "55", "40", "55"]
							},
							{
								fill: "true",
								label: "Revenue",
								backgroundColor: "transparent",
								borderWidth: 1,
								borderColor: "#5967d6",
								pointBorderColor: "#5967d6",
								pointBackgroundColor: "#fff",
								pointHoverBackgroundColor: "#fff",
								pointHoverBorderColor: "#5967d6",
								pointBorderWidth: 1,
								pointHoverBorderWidth: 1,
								tension: 0,
								stacked: false,
								data : ["30", "40", "33", "50", "43", "30", "60", "50", "70", "30", "50", "45", "65", "50", "70"]
							}
						]
					}
					
					if ($("#line-chart").length > 0) {
						
						var line_chart = new Chart(document.getElementById("line-chart").getContext("2d"), {
							type: 'line',
							data: data1,
							options: {
								responsive: true,
								legend: {
									display: true,
									labels: {
										boxWidth: 12,
										fontColor: "#838383",
										fontFamily: "Roboto",
										fontSize: 12,
										padding: 20
									}
								},
								tooltips: {
									enabled: false
								},
								scales: {
									xAxes: [{
										display: true,
									}],
									yAxes: [{
										display: true,
										ticks: {
											suggestedMin: 0,
											suggestedMax: 100,
										}
									}]
								}
							}
						});

					}
					
					
					// DOUGHNUT CHART //
					var data2 = {
						labels: [
							"Power",
							"Gas",
							"Oil"
						],
						datasets: [
						{
							data: [20, 10, 70],
							borderWidth: 0,
							backgroundColor: [
								"#4c3e99",
								"#72d3d5",
								"#ffffff"
							],
							hoverBackgroundColor: [
								"#4c3e99",
								"#72d3d5",
								"#ffffff"
							]
						}]
					};
					
					if ($("#doughnut-chart").length > 0) {
						
						var doughnut_chart = new Chart(document.getElementById("doughnut-chart").getContext("2d"), {
							type: 'doughnut',
							data: data2,
							options: {
								cutoutPercentage: 80,
								responsive: true,
								legend: {
									display: true,
									position: "bottom",
									labels: {
										boxWidth: 12,
										fontColor: "#fff",
										fontFamily: "Roboto",
										fontSize: 12,
										padding: 20
									}
								},
								tooltips: {
									enabled: false
								},
								scales: {
									xAxes: [{
										display: false
									}],
									yAxes: [{
										display: false,
									}]
								}
							}
						});

					}
					
					
					// PIE CHART //
					var data3 = {
						labels: [
							"Credibility",
							"Sustenability",
							"Economy"
						],
						datasets: [
						{
							data: [60, 25, 15],
							borderWidth: 0,
							backgroundColor: [
								"#4c3e99",
								"#a3d39c",
								"#6dcff6"
							],
							hoverBackgroundColor: [
								"#4c3e99",
								"#a3d39c",
								"#6dcff6"
							]
						}]
					};
					
					if ($("#pie-chart").length > 0) {
						
						var pie_chart = new Chart(document.getElementById("pie-chart").getContext("2d"), {
							type: 'pie',
							data: data3,
							options: {
								responsive: true,
								legend: {
									display: true,
									position: "bottom",
									labels: {
										boxWidth: 12,
										fontColor: "#838383",
										fontFamily: "Roboto",
										fontSize: 12,
										padding: 20
									}
								},
								tooltips: {
									enabled: false
								},
								scales: {
									xAxes: [{
										display: false
									}],
									yAxes: [{
										display: false,
									}]
								}
							}
						});

					}
					
					
					// BAR CHART //
					var data4 = {
						labels : ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
						datasets : [
							{
								label: "Profit",
								backgroundColor: "#5967d6",
								borderColor: "#fff",
								borderWidth: 3,
								hoverBorderWidth: 3,
								hoverBackgroundColor: "#5967d6",
								hoverBorderColor: "#fff",
								data : [80, 70, 60, 50, 80, 60, 55, 45, 35, 45, 50, 40]
							},
							{
								label: "Revenue",
								backgroundColor: "#72d3d5",
								borderColor: "#fff",
								borderWidth: 3,
								hoverBorderWidth: 3,
								hoverBackgroundColor: "#72d3d5",
								hoverBorderColor: "#fff",
								data : [70, 60, 55, 40, 100, 85, 75, 60, 50, 65, 70, 60]
							}
						]
					}
					
					if ($("#bar-chart").length > 0) {
						
						var bar_chart = new Chart(document.getElementById("bar-chart").getContext("2d"), {
							type: 'bar',
							data: data4,
							options: {
								responsive: true,
								legend: {
									display: true,
									labels: {
										boxWidth: 12,
										fontColor: "#838383",
										fontFamily: "Roboto",
										fontSize: 12,
										padding: 20
									}
								},
								tooltips: {
									enabled: true,
									xPadding: 15
								},
								scales: {
									xAxes: [{
										display: false
									}],
									yAxes: [{
										display: false,
										ticks: {
											suggestedMin: 0,
											suggestedMax: 100,
										}
									}]
								}
							}
						});

					}
					
					
					// AREA CHART //
					var data5 = {
						labels : ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
						datasets : [
							{
								fill: "true",
								label: "Profit",
								backgroundColor: "rgba(89, 103, 214, 0.2)",
								borderWidth: 1,
								borderColor: "#5967d6",
								pointBorderColor: "#5967d6",
								pointBackgroundColor: "#fff",
								pointHoverBackgroundColor: "#fff",
								pointHoverBorderColor: "#5967d6",
								pointBorderWidth: 1,
								pointHoverBorderWidth: 1,
								tension: 0.4,
								stacked: false,
								data : [55, 85, 65, 70, 40, 65, 75, 55, 70, 40, 65, 45]
							},
							{
								fill: "true",
								label: "Revenue",
								backgroundColor: "transparent",
								borderWidth: 1,
								borderColor: "#72d3d5",
								pointBorderColor: "#72d3d5",
								pointBackgroundColor: "#fff",
								pointHoverBackgroundColor: "#fff",
								pointHoverBorderColor: "#72d3d5",
								pointBorderWidth: 1,
								pointHoverBorderWidth: 1,
								tension: 0.4,
								stacked: false,
								data : [65, 75, 55, 65, 50, 75, 90, 80, 60, 50, 55, 70]
							}
						]
					}
					
					if ($("#area-chart").length > 0) {
						
						var area_chart = new Chart(document.getElementById("area-chart").getContext("2d"), {
							type: 'line',
							data: data5,
							options: {
								responsive: true,
								legend: {
									display: true,
									labels: {
										boxWidth: 12,
										fontColor: "#838383",
										fontFamily: "Roboto",
										fontSize: 12,
										padding: 20
									}
								},
								tooltips: {
									enabled: false
								},
								scales: {
									xAxes: [{
										display: true
									}],
									yAxes: [{
										display: true,
										ticks: {
											suggestedMin: 0,
											suggestedMax: 100,
										}
									}]
								}
							}
						});

					}
					
				}
				
			});
			
		}
		
	}
	
	
	// LOAD MORE PROJECTS //
	function load_more_projects() {
	
		var number_clicks = 0;
		
		$(".load-more").on("click", function(e) {
			
			e.preventDefault();
			
			if (number_clicks == 0) {
				$.ajax({
					type: "POST",
					url: $(".load-more").attr("href"),
					dataType: "html",
					cache: false,
					msg : '',
					success: function(msg) {
						$(".isotope").append(msg);	
						$(".isotope").imagesLoaded(function() {
							$(".isotope").isotope("reloadItems").isotope();
							$(".fancybox").fancybox({
								prevEffect: 'none',
								nextEffect: 'none',
								padding: 0
							});
						});
						number_clicks++;
						$(".load-more").html("Nothing to load");
					}
				});
			}
			
		});
		
	}
	
	
	// SHOW/HIDE SCROLL UP //
	function show_hide_scroll_top() {
		
		if ($(window).scrollTop() > $(window).height()/2) {
			$("#scroll-up").fadeIn(300);
		} else {
			$("#scroll-up").fadeOut(300);
		}
		
	}
	
	
	// SCROLL UP //
	function scroll_up() {				
		
		$("#scroll-up").on("click", function() {
			$("html, body").animate({
				scrollTop: 0
			}, 800);
			return false;
		});
		
	}
	
	
	// INSTAGRAM FEED //
	function instagram_feed() {

		if ($("#instafeed").length > 0 ) {
				
			var nr = $("#instafeed").data('number');
			var userid = $("#instafeed").data('user');
			var accesstoken = $("#instafeed").data('accesstoken');
			
			var feed = new Instafeed({
				target: 'instafeed',
				get: 'user',
				userId: userid,
				accessToken: accesstoken,
				limit: nr,
				resolution: 'thumbnail',
				sortBy: 'most-recent'
			});
			
			feed.run();
		
		}
		
	}
	
	
	// ANIMATIONS //
	function animations() {
		
		if (typeof WOW !== 'undefined') {
		
			animations = new WOW({
				boxClass: 'wow',
				animateClass: 'animated',
				offset: 100,
				mobile: false,
				live: true
			});
			
			animations.init();
		
		}
		
	}
	
	
	// EQUAL HEIGHT //
	function equal_height() {

		$(".text-boxes-list").each(function(){
			
			var x = 0;
			
			$(".text-boxes-list li").each(function() {
				
				if($(this).height() > x) {
					x = $(this).height();
				}
				
			});
			
			$(".text-boxes-list li .text-box").css("height", x + "px");

		});

	}
	
	
	// IMAGES BOXES //
	function images_boxes() {
		
		$(".image-box.style-2 .image-box-content").append('<a class="close-image-box-content" href="#">x</a>');
		
		$(".image-box.style-2 > h4").on("click", function() {
			$(this).fadeOut(300).next(".image-box.style-2 .image-box-content").addClass("slideup");
		});
			
		$(".close-image-box-content").on("click", function(e) {
			e.preventDefault();
			$(this).parents("div").removeClass("slideup");
			$(this).parents("div").prev("h4").fadeIn(300);
		});
		
	}
	
	
	// CALLOUT //
	function callout() {
		
		$(".callout").each(function() {
			
			var x = 0;
			
			$(this).find("li").each(function() {
				
				if($(this).height() > x) {
					x = $(this).height();
				}
				
			});
			
			$(this).find("li").css("height", x + "px");
		
		});
		
		$(".callout").on("click", function() {
			window.location = $(this).find("a").attr("href"); 
			return false;
		});
		
	}
	
	
	// FULL SCREEN //
	function full_screen() {

		if ($(window).width() > 767) {
			$(".full-screen").css("height", $(window).height() + "px");
		} else {
			$(".full-screen").css("height", "auto");
		}

	}
	
	
	// DOCUMENT READY //
	$(document).ready(function(){
		//document.querySelector('video').playbackRate = 0.5;
		// STICKY //
		if ($("body").hasClass("sticky-header")) {
			sticky();
		}
		
		
		// MENU //
		if (typeof $.fn.superfish !== 'undefined') {
			
			$(".menu").superfish({
				delay: 500,
				animation: {
					opacity: 'show',
					height: 'show'
				},
				speed: 'fast',
				autoArrows: true
			});
			
		}
		
		
		// SHOW/HIDE MOBILE MENU //
		show_hide_mobile_menu();
		
		
		// MOBILE MENU //
		mobile_menu();
		
		
		// HEADER SEARCH //
		header_search();
		
		
		// FOOTER PARALLAX //
		if ($("body").hasClass("footer-parallax")) {
			footer_parallax();
		}
		
		
		// FANCYBOX //
		if (typeof $.fn.fancybox !== 'undefined') {
		
			$(".fancybox").fancybox({
				prevEffect: 'none',
				nextEffect: 'none',
				padding: 0
			});
			
			$(".sign-in .btn").fancybox({
				maxWidth: 450,
				maxHeight: 380,
				fitToView: false,
				width: '90%',
				height: '90%',
				autoSize: false,
				closeClick: false,
				openEffect: 'fade',
				closeEffect: 'fade'
			});
		
		}
		
		// REVOLUTION SLIDER //
		if (typeof $.fn.revolution !== 'undefined') {
			
			$(".rev_slider").revolution({
				sliderType: "standard",
				sliderLayout: "auto",
				autoHeight: 'off',
				delay: 6000,
			   responsiveLevels: [1240, 1024, 778, 480],
			 
			    /* [DESKTOP, LAPTOP, TABLET, SMARTPHONE] */
			    gridwidth:[1240, 1024, 778, 400],
			 
			    /* [DESKTOP, LAPTOP, TABLET, SMARTPHONE] */
			    gridheight:[600, 600, 600, 450],				
				navigation: {
					arrows:{
						style: "zeus",
						enable: true,
						hide_onmobile: true,
						hide_onleave: false,
						hide_delay: 200,
						hide_delay_mobile: 1200,
						hide_under: 0,
						hide_over: 9999,
						tmp:'<div class="tp-title-wrap"><div class="tp-arr-imgholder"></div> </div>',
						left: {
							h_align: "left",
							v_align: "center",
							h_offset: 20,
							v_offset: 0
						 },
						 right: {
							h_align: "right",
							v_align: "center",
							h_offset: 20,
							v_offset: 0
						 }
					},
					bullets:{
						style: "custom",
						enable: true,
						hide_onmobile: false,
						hide_onleave: false,
						hide_delay: 200,
						hide_delay_mobile: 1200,
						hide_under: 0,
						hide_over: 9999,
						tmp: '', 
						direction: "horizontal",
						space: 10,       
						h_align: "center",
						v_align: "bottom",
						h_offset: 0,
						v_offset: 40
					},
					touch:{
						touchenabled: "on",
						swipe_treshold: 75,
						swipe_min_touches: 1,
						drag_block_vertical: false,
						swipe_direction: "horizontal"
					}
				}			
			});
			
		}
	
	
		// OWL Carousel //
		if (typeof $.fn.owlCarousel !== 'undefined') {
			
			// IMAGES SLIDER HORIZONTAL //
			$(".owl-carousel.images-slider-horizontal").owlCarousel({
				items: 1,
				autoplay: true,
				autoplayTimeout: 3000,
				autoplayHoverPause: true,
				smartSpeed: 1200,
				loop: true,
				nav: false,
				navText: false,
				dots: true,
				mouseDrag: true,
				touchDrag: true,
				animateIn: 'fadeIn',
				animateOut: 'fadeOut'
			});
			
			
			// IMAGES SLIDER VERTICAL //
			$(".owl-carousel.images-slider-vertical").owlCarousel({
				items: 1,
				autoplay: true,
				autoplayTimeout: 3000,
				autoplayHoverPause: true,
				smartSpeed: 1200,
				loop: true,
				nav: false,
				navText: false,
				dots: true,
				mouseDrag: true,
				touchDrag: true,
				animateIn: 'slideInDown',
				animateOut: 'slideOutDown'
			});
			
			
			// TESTIMONIALS SLIDER STYLE 1 //
			$(".owl-carousel.testimonials-slider.style-1").owlCarousel({
				items: 1,
				autoplay: true,
				autoplayTimeout: 3000,
				autoplayHoverPause: true,
				smartSpeed: 1200,
				loop: true,
				nav: false,
				navText: false,
				dots: true,
				mouseDrag: true,
				touchDrag: true,
				animateIn: 'fadeIn',
				animateOut: 'fadeOut'
			});
			
			
			// TESTIMONIALS SLIDER STYLE 2 //
			$(".owl-carousel.testimonials-slider.style-2").owlCarousel({
				autoplay: true,
				autoplayTimeout: 3000,
				autoplayHoverPause: true,
				smartSpeed: 500,
				loop: true,
				nav: false,
				navText: false,
				dots: true,
				mouseDrag: true,
				touchDrag: true,
				margin: 30,
				responsive: {
					0:{
						items: 1
					},
					768:{
						items: 2
					},
					992:{
						items: 3
					}
				}
			});
			
			
			// TESTIMONIALS SLIDER STYLE 3 //
			var $testimonial_author_image = $(".testimonial-author-image"),
				$testimonials = $(".testimonials"),
				flag = false,
				duration = 500;

			$testimonial_author_image.owlCarousel({
				items: 1,
				autoplay: true,
				autoplayTimeout: 3000,
				autoplayHoverPause: true,
				smartSpeed: 500,
				nav: false,
				dots: false,
				mouseDrag: false,
				touchDrag: true
			})
			.on('changed.owl.carousel', function (e) {
				if (!flag) {
					flag = true;
					$testimonials.trigger('to.owl.carousel', [e.item.index, duration, true]);
					flag = false;
				}
			});

			$testimonials.owlCarousel({
				items: 1,
				autoplay: true,
				autoplayTimeout: 3000,
				autoplayHoverPause: true,
				smartSpeed: 500,
				nav: false,
				dots: true,
				mouseDrag: false,
				touchDrag: true
			})
			.on('click', '.owl-item', function () {
				$testimonial_author_image.trigger('to.owl.carousel', [$(this).index(), duration, true]);

			})
			.on('changed.owl.carousel', function (e) {
				if (!flag) {
					flag = true;		
					$testimonial_author_image.trigger('to.owl.carousel', [e.item.index, duration, true]);
					flag = false;
				}
			});
			
			
			// LOGOS SLIDER //
			$(".owl-carousel.logos-slider").owlCarousel({
				autoplay: true,
				autoplayTimeout: 3000,
				autoplayHoverPause: true,
				smartSpeed: 1200,
				loop: true,
				nav: true,
				navText: false,
				dots: false,
				mouseDrag: true,
				touchDrag: true,
				responsive: {
					0:{
						items: 1
					},
					480:{
						items: 2
					},
					768:{
						items: 3
					},
					992:{
						items: 4
					},
					1200:{
						items: 5
					}
				}
			});
			
			
			/* TIMELINE SLIDER */
			var timeline_slider = $(".owl-carousel.timeline-slider").owlCarousel({
				items: 1,
				autoplay: false,
				smartSpeed: 200,
				loop: true,
				nav: false,
				navText: false,
				dots: false,
				mouseDrag: false,
				touchDrag: false,
				animateIn: 'fadeIn',
				animateOut: 'fadeOut'
			});
			
			$(".timeline-slider-controls li").on("click", function() {
				timeline_slider.trigger('to.owl.carousel',[$(this).index(), 300, true]);
			});
			
			
			/* TIMELINE SLIDER 2 */
			var timeline_slider_2 = $(".owl-carousel.timeline-slider-2").owlCarousel({
				items: 1,
				autoplay: false,
				smartSpeed: 200,
				loop: true,
				nav: false,
				navText: false,
				dots: false,
				mouseDrag: false,
				touchDrag: false,
				animateIn: 'fadeIn',
				animateOut: 'fadeOut'
			});
			
			$(".timeline-slider-2-controls li").on("click", function() {
				$(".timeline-slider-2-controls li").removeClass("active");
				$(this).addClass("active");
				timeline_slider_2.trigger('to.owl.carousel',[$(this).index(), 300, true]);
			});
		
		}
		
		
		// GOOGLE MAPS //
		if (typeof $.fn.gmap3 !== 'undefined') {
		
			$(".map").each(function() {
				
				var data_zoom = 15,
					data_height,
					data_popup = false;
				
				if ($(this).attr("data-zoom") !== undefined) {
					data_zoom = parseInt($(this).attr("data-zoom"),10);
				}	
				
				if ($(this).attr("data-height") !== undefined) {
					data_height = parseInt($(this).attr("data-height"),10);
				}
				
				if ($(this).attr("data-address-details") !== undefined) {
					
					data_popup = true;
					
					var infowindow = new google.maps.InfoWindow({
						content: $(this).attr("data-address-details")
					});
					
				}
				
				
				$(this)
				.gmap3({
					address: $(this).attr("data-address"),
					zoom: data_zoom,
					mapTypeId: google.maps.MapTypeId.ROADMAP,
					scrollwheel: false
				})
				.marker([
					{address: $(this).attr("data-address")}
				])
				.on({
					click: function(marker, event){
						if (data_popup) {
							infowindow.open(marker.get('map'), marker);
						}
					}
				});
				  
				$(this).css("height", data_height + "px");
				
			});
			
		}
		
		
		// ISOTOPE //
		if ((typeof $.fn.imagesLoaded !== 'undefined') && (typeof $.fn.isotope !== 'undefined')) {
		
			$(".isotope").imagesLoaded( function() {
				
				var container = $(".isotope");
				
				container.isotope({
					itemSelector: '.isotope-item',
					layoutMode: 'masonry',
					transitionDuration: '0.8s'
				});
				
				$(".filter li a").on("click", function() {
					$(".filter li a").removeClass("active");
					$(this).addClass("active");
		
					var selector = $(this).attr("data-filter");
					container.isotope({
						filter: selector
					});
		
					return false;
				});
		
				$(window).resize(function() {
					container.isotope();
				});
				
			});
			
		}
		
		
		// LOAD MORE PORTFOLIO ITEMS //
		load_more_projects();
		
		
		// PLACEHOLDER //
		if (typeof $.fn.placeholder !== 'undefined') {
			
			$("input, textarea").placeholder();
			
		}
		
		
		// CONTACT FORM VALIDATE & SUBMIT //
		// VALIDATE //
		if (typeof $.fn.validate !== 'undefined') {
		
			$("#contact-form").validate({
				rules: {
					name: {
						required: true
					},
					email: {
						required: true,
						email: true
					},
					subject: {
						required: true
					},
					message: {
						required: true,
						minlength: 10
					}
				},
				messages: {
					name: {
						required: "Please enter your name!"
					},
					email: {
						required: "Please enter your email!",
						email: "Please enter a valid email address"
					},
					subject: {
						required: "Please enter the subject!"
					},
					message: {
						required: "Please enter your message!"
					}
				},
					
				// SUBMIT //
				submitHandler: function(form) {
					var result;
					$(form).ajaxSubmit({
						type: "POST",
						data: $(form).serialize(),
						url: "assets/php/send.php",
						success: function(msg) {
							
							if (msg == 'OK') {
								result = '<div class="alert alert-success">Your message was successfully sent!</div>';
								$("#contact-form").clearForm();
							} else {
								result = msg;
							}
							
							$("#alert-area").html(result);
		
						},
						error: function() {
		
							result = '<div class="alert alert-danger">There was an error sending the message!</div>';
							$("#alert-area").html(result);
		
						}
					});
				}
			});
			
		}
		
		
		// PARALLAX //
		if (typeof $.fn.stellar !== 'undefined') {
		
			if (!is_touch_device()) {
				
				$(window).stellar({
					horizontalScrolling: false,
					verticalScrolling: true,
					responsive: true
				});
				
			} else {
				
				$(".parallax").addClass("parallax-disable");
				
			}
		
		}
		
		
		// SHOW/HIDE SCROLL UP
		show_hide_scroll_top();
		
		
		// SCROLL UP //
		scroll_up();
		
		
		// PROGRESS BARS //
		progress_bars();
		
		
		// PIE CHARTS //
		pie_chart();
		
		
		// COUNTER //
		counter();
		
		
		// STATISTICS //
		statistics();
		
		
		// YOUTUBE PLAYER //
		if (typeof $.fn.mb_YTPlayer !== 'undefined') {
			
			$(".youtube-player").mb_YTPlayer();
		
		}
		
		
		// INSTAGRAM FEED //
		instagram_feed();
		
		
		// TWITTER //
		if(typeof twitterFetcher !== 'undefined' && ($('.widget-twitter').length > 0)) {
			
			$('.widget-twitter').each(function(index){
			
				var account_id = $('.tweets-list', this).attr('data-account-id'),
					items = $('.tweets-list', this).attr('data-items'),
					newID = 'tweets-list-' + index;
				
				$('.tweets-list', this).attr('id', newID);
				
				var config = {
				  "id": account_id,
				  "domId": newID,
				  "maxTweets": items,
				  "showRetweet": false,
				  "showTime": false,
				  "showUser": false,
				  "showInteraction": false
				};
				
				twitterFetcher.fetch(config);
			});
			
		}
		
		
		// COUNTDOWN //
		if (typeof $.fn.countdown !== 'undefined') {
			
			$(".countdown").countdown('2018/1/31 00:00', function(event) {
				$(this).html(event.strftime(
					'<div><div class="count">%-D</div> <span>Days</span></div>' +
					'<div><div class="count">%-H</div> <span>Hours</span></div>' +
					'<div><div class="count">%-M</div> <span>Minutes</span></div>' +
					'<div><div class="count">%S</div> <span>Seconds</span></div>'
				));
			});
		
		}
		
		
		// ANIMATIONS //
		animations();
		
		
		// EQUAL HEIGHT //
		equal_height();
		
		
		// IMAGES BOXES //
		images_boxes();
		
		
		// CALLOUT //
		callout();
		
		
		// FULL SCREEN //
		full_screen();
		
	});

	
	// WINDOW SCROLL //
	$(window).scroll(function() {
		
		progress_bars();
		pie_chart();
		counter();
		statistics()
		show_hide_scroll_top();
		
	});
	
	
	// WINDOW RESIZE //
	$(window).resize(function() {

		mobile_menu();
		equal_height();
		callout();
		full_screen();
		
		if ($("body").hasClass("footer-parallax")) {
			footer_parallax();
		}
		
	});
	
	
	// WINDOW LOAD //
	$(window).load(function() {
		
		page_loader();
		
	});
	
})(window.jQuery);