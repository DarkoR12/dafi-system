from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView

from ..models import TradeOffer, TradeOfferAnswer

from .common import TradingPeriodMixin


class TradeOfferAnswerDetailView(UserPassesTestMixin, DetailView):
    model = TradeOfferAnswer

    template_name = 'trading/answer_detail.html'

    def test_func(self):
        answer = self.get_object()
        user = self.request.user

        return user.has_perm('trading.is_manager') or user == answer.offer.user or user == answer.user


class TradeOfferAnswerEditMixin(TradingPeriodMixin):
    def post(self, request, **kwargs):
        offer = self.get_offer()
        answer = self.get_answer()

        data = {}

        for line in offer.lines.all():
            try:
                data[line.year.id] = [
                    int(request.POST.get('{}-group'.format(line.i))),
                    int(request.POST.get('{}-subgroup'.format(line.i))),
                ]
            except TypeError:
                return super().get(request, **kwargs)

        answer.set_groups(data)

        try:
            answer.save()
        except ValidationError:
            return super().get(request, **kwargs)

        return self.on_success(request, **kwargs)


class TradeOfferAnswerCreateView(LoginRequiredMixin, UserPassesTestMixin, TradeOfferAnswerEditMixin, DetailView):
    model = TradeOffer
    template_name = 'trading/answer_form.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._answer = None

    def test_func(self):
        offer = self.get_object()

        if self.request.user == offer.user:
            return False

        return TradeOfferAnswer.objects.filter(user=self.request.user, offer=offer).count() == 0

    def get_offer(self):
        return self.get_object()

    def get_answer(self):
        if not self._answer:
            self._answer = TradeOfferAnswer(offer=self.get_offer(), user=self.request.user)

        return self._answer

    def on_success(self, request, **kwargs):
        return redirect(reverse_lazy('trading:answer_detail', args=[self.get_answer().id]))


class TradeOfferAnswerAccessMixin(UserPassesTestMixin, TradingPeriodMixin):
    def test_func(self):
        answer = self.get_object()

        return self.request.user == answer.user and not answer.offer.answer


class TradeOfferAnswerEditView(TradeOfferAnswerAccessMixin, TradeOfferAnswerEditMixin, DetailView):
    model = TradeOfferAnswer
    template_name = 'trading/answer_edit.html'

    def get_offer(self):
        return self.get_object().offer

    def get_answer(self):
        return self.get_object()

    def on_success(self, request, **kwargs):
        return super().get(request, **kwargs)


class TradeOfferAnswerDeleteView(TradeOfferAnswerAccessMixin, DeleteView):
    model = TradeOfferAnswer
    template_name = 'trading/answer_delete.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('trading:list')


class TradeOfferAnswerAcceptView(UserPassesTestMixin, TradingPeriodMixin, DetailView):
    model = TradeOfferAnswer

    template_name = 'trading/answer_accept.html'

    def test_func(self):
        answer = self.get_object()

        return self.request.user == answer.offer.user and not answer.offer.answer

    def post(self, request, **kwargs):
        answer = self.get_object()
        answer.offer.answer = answer
        answer.save()

        return reverse_lazy('trading:change_process', args=[answer.offer.id])