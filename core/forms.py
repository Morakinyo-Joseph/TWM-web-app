from django import forms

class BoardPlacementForm(forms.Form):
    CHOICES = [
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
        ('6','6'),
        ('7','7'),
        ('8','8'),
        ('9','9'),
    ]

    post = forms.CharField(label='Choose your next post', widget=forms.RadioSelect(choices=CHOICES))


class WhitePieceForm(forms.Form):
    PIECES = [
        ('w1', 'w1'),
        ('w2', 'w2'),
        ('w3', 'w3'),
    ]
    piece = forms.CharField(label="Select a piece to move", widget=forms.RadioSelect(choices=PIECES))


class BlackPieceForm(forms.Form):
    PIECES = [
        ('b1', 'b1'),
        ('b2', 'b2'),
        ('b3', 'b3'),
    ]
    piece = forms.CharField(label="Select a piece to move", widget=forms.RadioSelect(choices=PIECES))
    