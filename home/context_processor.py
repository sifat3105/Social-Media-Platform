from django.urls import reverse



def profile(r):
    if r.user.is_authenticated:
        if hasattr(r.user, 'account'):
            if r.user.profile.image:
                profile_icon = r.user.profile.image.url
            else:
                profile_icon = '/static/assets/images/account.png'
        else:
            profile_icon = '/static/assets/images/account.png'
            
        username= r.user.username
        log_reg_link = reverse('login')
        # log_reg_link = reverse('account', kwargs={'username': username})
    else:
        profile_icon = '/static/assets/images/account.png'
        log_reg_link = reverse('login')
        
    
    return {
        'profile_icon': profile_icon,
        'log_reg_link': log_reg_link,
       
    }