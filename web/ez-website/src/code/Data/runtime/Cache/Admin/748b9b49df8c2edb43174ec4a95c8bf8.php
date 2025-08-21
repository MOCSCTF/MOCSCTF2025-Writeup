<?php if (!defined('THINK_PATH')) exit();?><!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3c.org/TR/1999/REC-html401-19991224/loose.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>管理登录_<?php echo ($WebName); ?></title>
<meta content="zh-cn" http-equiv="content-language" />
<meta content="text/html; charset=utf-8" http-equiv="content-type" />
<meta name="renderer" content="webkit">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
<meta name="generator" content="YoudianCMS" data-variable="http://www.youdiancms.com" />
<link href="<?php echo ($Css); ?>font.css" rel="stylesheet" type="text/css" />
<link href="<?php echo ($WebPublic); ?>jquery/ui-dialog.css" rel="stylesheet" type="text/css" />
<style>
body {
	padding: 0; margin: 0; height: 100%; overflow: hidden; 
	background: #fafafa;
	font-size:12px;
	font-family: "Microsoft Yahei";
}
img {padding: 0;  margin: 0; border-width:0; float: none; }
a { outline-style: none;}
form {padding:0; margin: 0px; }
table {border-collapse: collapse}
tr {padding: 0;  margin: 0px; border-width: 0px;float: none; }
* {padding: 0px; margin: 0px; }
input {padding-bottom: 2px; padding-left: 2px; padding-right: 2px; font-size: 12px; padding-top: 2px;}
a {color: #4a4a4a; font-size: 12px; text-decoration: none;}
a:visited {color: #4a4a4a; font-size: 12px; text-decoration: none;}
a:hover {color: #fb5118; font-size: 12px; text-decoration: none;}

input.infoinput {
	border: 0; border-bottom: 1px solid #ddd; background: #fff; padding: 13px 5px; margin: 3px 0; margin-left: 20px;
	font-size: 16px; box-sizing: border-box; transition: all .3s; outline: none;
}
input.infoinput:focus {
	border-color: <?php echo ($AdminThemeColor); ?>;
}
input.buttonface {
	border: 0; outline: none; border: 0; cursor: pointer; margin-top: 40px;
    height: 40px; line-height: 40px; width: 100%; text-align: center; font-size: 15px; color: #FFF; border-radius: 4px; 
	background: <?php echo ($AdminThemeColor); ?>;
}
input.buttonface:hover { opacity:0.8; }
input.buttonface:active{ box-shadow: inset 0 3px 5px rgba(0,0,0,.125); }
input.buttonface.buttonface[disabled]{ background:#ccc;}
.logo{ position: fixed; left: 10px; top: 10px; }
.logo img{ height:50px;}
.login-div {
	text-align: center; padding-bottom: 0px; margin: 0px auto; padding-left: 0px; width: 100%; padding-right: 0px; 
}
.login-top {
	width: 520px; display: block; float: left; height: 35px;
}
.login-down {
	width: 520px; display: block; height: 30px;
}
.login-bg {
	width: 520px; 
}
.login {text-align: left; padding: 0 25px 24px 25px;}
.loigntitle { color: #000; font-size: 26px; float: left;}
.loign-line {margin: 0px auto; padding-left: 15px;}
.login-form-center {text-align: left; padding:0 40px; overflow: hidden;}
.logintd img{ width: 22px; }
.loginwanntile {
	color: #8a6d3b; border-radius: 4px;
    background-color: #fcf8e3;
    border: 1px solid #faebcc;
	text-align: left; width: 173px; margin-bottom: 5px; margin-top: 10px; clear: both; overflow: hidden;
}
.loginwanntile ul {padding-bottom: 2px; line-height: 30px; list-style-type: none; padding-left: 2px; padding-right: 2px; height: 30px; padding-top: 2px;}
.loginwanntile ul li {
	padding-left: 10px; color: #cf6b47;
}
#centerlogin {margin: 0px auto; width: 520px; border-collapse: collapse;}
.login-form {width: 520px; float: left; overflow: hidden; background: #FFF; border-radius: 10px; box-shadow: 0 5px 18px 0 rgba(0,0,0,.1); }
.fotter { position: fixed; bottom: 20px; line-height: 20px; width: 520px; height: 20px; color: gray; overflow: hidden;}
#AuthorizeImage{ padding-left: 6px; height:42px; }
.BindUc0{ float: right;}
#AuthorizeImage img{ vertical-align: bottom; }
.license{ padding-top:10px; font-size: 14px;}
.license .btnxy{vertical-align:middle;}
.license .xy-name{ 
	color:<?php echo ($AdminThemeColor); ?>; font-size:14px; cursor:pointer;
}
.license a{ 
	color:<?php echo ($AdminThemeColor); ?>; font-size:14px; 
}
.license a:hover{ opacity:0.8; }
#dlgLicense{ width: 900px; height: 520px; display: none; overflow:auto;}

.ui-dialog-footer button.ui-dialog-autofocus,
.ui-dialog-footer button.ui-dialog-autofocus:hover,
.ui-dialog-footer button.ui-dialog-autofocus:focus,
.ui-dialog-footer button.ui-dialog-autofocus:active,
.ui-dialog-footer button.ui-dialog-autofocus{ 
	background-color: <?php echo ($AdminThemeColor); ?>;
	border-color:<?php echo ($AdminThemeColor); ?>;
}
.ui-dialog-footer button:focus {outline: none;}
.ui-dialog-footer button.ui-dialog-autofocus:hover{ opacity:0.8; }
.ui-dialog-footer { padding: 12px 15px; border-top:1px solid #e5e5e5;}

.login-way{ overflow: hidden;  margin-right: 5px; margin-top: 5px;}
.login-way p{ font-size: 14px;  float: right; box-shadow: 0 2px 8px rgba(0,0,0,.15);
    border-radius: 4px; padding: 6px 10px;margin-top: 8px;}
.login-way img{ width: 45px;height: 45px;  vertical-align: middle;float: right;}
.login-way1,.login-way2{ float: right; cursor: pointer; display: none;}
/*登录二维码*/
#frmLogin{ display: none;}
#login-qrcode{ overflow: hidden; display: none;text-align: center;}
#login-qrcode img{ width: 170px; margin: 3px 0; border: 1px solid #ddd;}
#login-qrcode .qrcode-title{ font-size:18px; text-align: center; padding: 3px 0; margin-top: 3px;}
</style>
</head>
<body>
	<div class="logo">
		<?php if(empty($IsOem)): ?><img src="<?php echo ($Images); ?>login_logo.png" />
		<?php else: ?>
			<?php if(!empty($CmsLoginLogo)): ?><img src="<?php echo ($CmsLoginLogo); ?>" /><?php endif; endif; ?>
	</div>
	<div class="login-div">
		<table id="centerlogin" border="0" cellpadding="0" width="100%">
		  <tbody>
		  <tr>
		    <td style="width: 520px" valign="center" align="middle">
		      <div class="login-form">
		      <table style="border-collapse: collapse" border="0" cellpadding="0" width="520"><tbody>
		        <tr>
					<td class="login-top">
						<?php if(!empty($IsBindUc)): ?><div class="login-way">
								<div class="login-way1" onclick="changeLoginWay(1)">
									<img src="data:image/png;base64,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" />
									<p>账号密码登录</p>
								</div>
								<div class="login-way2" onclick="changeLoginWay(2)">
									<img src="data:image/png;base64,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" />
									<p>微信扫码登录</p>
								</div>
							</div><?php endif; ?>
					</td>
				</tr>
		        <tr>
		          <td class="login-bg">
		            <table style="width: 100%">
		              <tbody>
						<tr>
							<td class="login">
								<div class="loigntitle">管理员登录</div>
								<span id="AuthorizeImage" class="BindUc<?php echo ($IsBindUc); ?>"></span>
							</td>
						</tr>
						<tr>
							<td>
							<table style="width: 100%">
								<tbody>
								<tr>
								<td class="login-form-center">
									<form id="frmLogin" method="post" name="frmLogin" action="<?php echo ($Url); ?>checkLogin/"  enctype="multipart/form-data">
									<table border="0" cellpadding="0">
										<tbody>
										
										<tr>
											<td class="logintd" nowrap="nowrap"><img src="<?php echo ($Images); ?>user.png"></td>
											<td class="logintd2">
											<input style="width: 390px" placeholder="请输入用户名" id="username" class="infoinput" maxlength="20" name="username" value="">
											</td>
										</tr>
										<tr>
											<td class="logintd"><img src="<?php echo ($Images); ?>pwd.png"></td>
											<td class="logintd2">
											<input style="width: 390px" placeholder="请输入密码"  id="password" class="infoinput" maxlength="20" type="password" name="password" value="" autocomplete="off"></td>
										</tr>
										<tr class="vc" style="display:none;">
											<td class="logintd"><img src="<?php echo ($Images); ?>code.png" /></td>
											<td class="logintd2">
												<input style="text-transform: uppercase; width: 120px; margin-right:2px;" id="verifycode" class="infoinput" placeholder="请输入验证码" maxlength="4" name="verifycode" value="">
												<img style="cursor: pointer; height: 25px;" id="verifycodeimg" title="如果您无法识别验证码，请点图片更换" src="<?php echo ($Url); ?>verify/" align="absMiddle" />
											</td>
										</tr>
										<tr>
											<td class="logintd2" colspan="2"><input class="buttonface" value="登录" type="submit" name="button"></td>
										</tr>
										<?php if(empty($IsOem)): ?><tr>
											<td  colspan="2" class="license" valign="middle">
												<label><input class="btnxy" value="1"  type="checkbox" name="btnxy"> 我已阅读并同意</label>
												<span class='xy-name'>《最终用户授权许可协议》</span>
											</td>
										</tr><?php endif; ?>
										</tbody>
									</table>
									</form>
									<div id="login-qrcode">
										<img src="data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==" />
										<div class="qrcode-title">微信扫码登录</div>
									</div>
								</td>
								</tr>
							</tbody>
							</table>
						</td>
						</tr>
		             </tbody>
		          </table>
		          </td>
		       </tr>
		        <tr><td class=login-down></td></tr></tbody></table></div>
		      <div class="fotter">
				<?php if(empty($IsOem)): ?><a href="<?php echo ($CompanyUrl1); ?>" target="_blank"><?php echo ($CMSName); echo ($CMSEnName); echo ($CMSVersion); ?></a>&nbsp;
					<a href="<?php echo ($CompanyUrl1); ?>" target="_blank"><?php echo ($CompanyFullName); ?></a>
					&nbsp;&nbsp;版权所有&nbsp;&nbsp;侵权必究<?php endif; ?>
		      </div>
		      </td></tr></tbody>
		</table>
	</div>
</body>
</html>
<div class="dialog" id="dlgLicense" title="最终用户授权许可协议">
<?php echo ($LicenseContent); ?>
</div>
<script type="text/javascript" src="<?php echo ($WebPublic); ?>jquery/jquery.min.js"></script>
<script type="text/javascript" src="<?php echo ($WebPublic); ?>jquery/crypto-js.min.js"></script>
<script type="text/javascript" src="<?php echo ($WebPublic); ?>jquery/dialog-plus-min.js"></script>
<script type="text/javascript">
function AlertTip(msg){
	var title = '友情提示';
	msg = "<div id='icon_warning' style='text-align:left; width: 260px;font-size:16px;padding:8px 0;'>"+msg+"</div>";
	var d= dialog({
		title:title, skin:'warning-box',padding:8, content:msg, id:'msgtipid',
		ok: function () {
			return true;
		},
		okValue: '确定'
	});
	d.show();
	return d;
}

function SafeCode(str){
	var chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
	str = btoa(encodeURIComponent(str));
	var len = 6;
	var prefix = '';
	for (var i = len; i > 0; --i){
		prefix += chars[Math.floor(Math.random() * chars.length)];
	}
	var suffix = '';
	for (var i = len; i > 0; --i){
		suffix += chars[Math.floor(Math.random() * chars.length)];
	}
	str = prefix+str+suffix;
	return str;
}

	$(document).ready(function(){
		window.localStorage.removeItem("AdminLoginName");
		window.localStorage.removeItem("IsSafeAnswer");
		window.localStorage.removeItem("YDCurrentDir1");  //文件管理器默认目录
		
		var isAgree = parseInt("<?php echo ($IsAgree); ?>");
		if(isAgree){
			$(".btnxy").prop('checked', true);
		}
		
			function ChangeVerify(){
				var timenow = new Date().getTime();
				$("#verifycodeimg").attr("src", "<?php echo ($Url); ?>verify/d/" + timenow);
			};
			
			$("#username").blur(function(){
				var username = $("#username").val();
				if( username.length > 0 ){
					var url = "<?php echo ($Group); ?>/Public/showCode";
					var timenow = new Date().getTime();
					var p = {username: username, random: timenow};
					$.get(url, p, function(data){
						if( data.status == 1 ) {
							$(".vc").show();
						}else{
							$(".vc").hide();
						}
					}, "json");
				}
			});
			
			 $('#frmLogin').submit(function(){
				 var isOem = "<?php echo ($IsOem); ?>";
				 if(0==isOem){
				 	 var  isAgree = $(".btnxy").is(':checked');
					 if(!isAgree){
						AlertTip("请阅读并同意协议！");
						return false;
					 }
				 }

				 
				 var username = $("#username").val();
				 var password = $("#password").val();
				 if(username==""){
					AlertTip("用户名不能为空");
					$("#username").focus();
					return false;	 
				 }
				 if(password==""){
					AlertTip("密码不能为空");
					$("#password").focus();
					return false;	 
				 }
				 password = SafeCode(password);
				 username = CryptoJS.MD5(username).toString();
				 var params = {
					username: username, 
					password: password, 
					verifycode:$("#verifycode").val() 
				};
				 var url = "<?php echo ($Url); ?>checkLogin/";
				 $.post(url, params, function(data){
						if (data.status==0){
							if( data.data == 1 ) {
								ChangeVerify();
								$(".vc").show();
							}else{
								$(".vc").hide();
							}
							AlertTip(data.info);
						}else if(data.status==1 || data.status == 2){
							AlertTip(data.info);
						}else if(data.status==3){  //登录成功
							window.location = '<?php echo ($Url); ?>adminIndex';
						}
				 }, "json"); 
				 //为了防止普通浏览器进行表单提交和产生页面导航（防止页面刷新？）返回false  
				return false; 
			 });
			 
			 //查看协议
			 $(".xy-name").click(function(){
				showLicenseDlg();
			 });
			 
			 function showLicenseDlg(){
			 	dialog({
					title: $("#dlgLicense").attr("title"),
					id: 'dialog-license',
					padding: 8,
					content: document.getElementById('dlgLicense'),
					ok: function () {
						$(".btnxy").prop('checked', true);
					},
					okValue: '同意',
					cancelValue: '不同意',
					cancel: function () {
						$(".btnxy").prop('checked', false);
					}
				}).show();
			 }
			 
			 pageInit();
			 function pageInit(){
				var h = $(window).height();
				$('#centerlogin').css({ height: h });
				$("#verifycodeimg").click( ChangeVerify );
			 	$('#username').focus();
			 }
	});

	var resizeTimer = null;
	function sizewindow(){
		var h = $(window).height();
		$('#centerlogin').css({height:h});
	}
	window.onresize=sizewindow;
	if(self!=top){top.location=self.location;}
</script>

<script>
	var gTimerID = null;
	var gRefreshTimerID = null;
	$(document).ready(function(){
		var IsBindUc = parseInt("<?php echo ($IsBindUc); ?>");
		if(0==IsBindUc) { //如果只有1种登录方式
			$("#frmLogin").show();
			return;
		}
		var loginWay = window.localStorage.getItem("LoginWay") || 1;
		changeLoginWay(loginWay);
	});

	//定时刷新二维码
	function getLoginQrcode(){
		var url = "<?php echo ($Url); ?>getLoginQrcode";
		$.post(url, null, function(res){
			console.log("getLoginQrcode", res);
			if(res.Status==1){
				var SceneStr = res.Data.SceneStr;
				$("#login-qrcode img").attr("src", res.Data.Qrcode);
				checkLoginQrcode(SceneStr);
			}else{
				AlertTip(res.Message);
			}
		},"json")
	}

	//改变登录方式
	function changeLoginWay(way){
		window.localStorage.setItem("LoginWay", way);
		if(1 == way){ //账号密码登录
			clearCheckTimer();
			clearRefreshTimer();
			$(".login-way2,#frmLogin").show();
			$(".login-way1,#login-qrcode").hide();
		}else{ //扫码登录
			$(".login-way2,#frmLogin").hide();
			$(".login-way1,#login-qrcode").show();
			getLoginQrcode();
			gRefreshTimerID = setInterval(function(){
				getLoginQrcode();
			}, 300*1000); //默认5分钟刷新一次二维码
		}
	}

	//定时检查登录是否成功
	function checkLoginQrcode(SceneStr){
		clearCheckTimer(); //防止重复执行定时器
		gTimerID = setTimeout(function(){
			var url = "<?php echo ($Url); ?>checkLoginQrcode";
			var params = {
				SceneStr:SceneStr,
			};
			$.post(url, params, function(res){
				if(res.status == 3){ //登录成功
					clearCheckTimer();
					clearRefreshTimer();
					window.location = '<?php echo ($Url); ?>AdminIndex';
				}else{
					checkLoginQrcode(SceneStr);
				}
			},"json")
		}, 1800);
	}

	function clearCheckTimer(){
		if(gTimerID > 0){
			clearTimeout(gTimerID);
			gTimerID = null;
		}
	}

	function clearRefreshTimer(){
		if(gRefreshTimerID > 0){
			clearInterval(gRefreshTimerID);
			gRefreshTimerID = null;
		}
	}
</script>