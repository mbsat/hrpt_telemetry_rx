#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: NOAA HRPT Receiver from baseband file
# Author: Martin Blaho
# Description: Demodulate, decode HRPT signal to minor frames
# Generated: Thu Jul 14 12:19:31 2011
##################################################

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import noaa
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
from time import strftime, localtime, gmtime
import math, os
import poesweather
import wx

class bb_rx_noaa_hrpt_fr_ver2(grc_wxgui.top_block_gui):

	def __init__(self, satellite='NOAAxx', decim=50, baseband_file="/home/martin/GNURadioData/hrpt/baseband/HRPT_NOAA19_2010-09-10_12-35-34_UTC_U2_d50.sam", frames_file=os.environ['HOME'] + '/noaa_hrpt_frames.hmf', deframer_outsync_frames=5, deframer_insync_frames=2, clock_alpha=0.005, gain_mu=0.005, pll_alpha=0.005, pll_beta=0.00001, deframer_sync_check=True, symb_rate=600*1109):
		grc_wxgui.top_block_gui.__init__(self, title="NOAA HRPT Receiver from baseband file")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Parameters
		##################################################
		self.satellite = satellite
		self.decim = decim
		self.baseband_file = baseband_file
		self.frames_file = frames_file
		self.deframer_outsync_frames = deframer_outsync_frames
		self.deframer_insync_frames = deframer_insync_frames
		self.clock_alpha = clock_alpha
		self.gain_mu = gain_mu
		self.pll_alpha = pll_alpha
		self.pll_beta = pll_beta
		self.deframer_sync_check = deframer_sync_check
		self.symb_rate = symb_rate

		##################################################
		# Variables
		##################################################
		self.decim_tb = decim_tb = decim
		self.symb_rate_tb = symb_rate_tb = symb_rate
		self.samp_rate = samp_rate = 100e6/decim_tb
		self.sps = sps = samp_rate/symb_rate_tb
		self.satellite_text = satellite_text = satellite
		self.samp_rate_st = samp_rate_st = samp_rate
		self.pll_beta_sl = pll_beta_sl = pll_beta
		self.pll_alpha_sl = pll_alpha_sl = pll_alpha
		self.max_clock_offset = max_clock_offset = 0.1
		self.max_carrier_offset = max_carrier_offset = 2*math.pi*100e3/samp_rate
		self.hs = hs = int(sps/2.0)
		self.gain_mu_sl = gain_mu_sl = gain_mu
		self.frames_file_text_inf = frames_file_text_inf = frames_file
		self.deframer_sync_after_text = deframer_sync_after_text = deframer_insync_frames
		self.deframer_nosync_after_text = deframer_nosync_after_text = deframer_outsync_frames
		self.deframer_check_sync_text = deframer_check_sync_text = deframer_sync_check
		self.datetime_text = datetime_text = strftime("%A, %B %d %Y %H:%M:%S", localtime())
		self.clock_alpha_sl = clock_alpha_sl = clock_alpha
		self.baseband_file_text_inf = baseband_file_text_inf = baseband_file

		##################################################
		# Notebooks
		##################################################
		self.rx_ntb = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
		self.rx_ntb.AddPage(grc_wxgui.Panel(self.rx_ntb), "Input baseband")
		self.rx_ntb.AddPage(grc_wxgui.Panel(self.rx_ntb), "PLL demodulator and Clock sync")
		self.rx_ntb.AddPage(grc_wxgui.Panel(self.rx_ntb), "Deframer")
		self.rx_ntb.AddPage(grc_wxgui.Panel(self.rx_ntb), "Output")
		self.Add(self.rx_ntb)

		##################################################
		# Controls
		##################################################
		self._decim_tb_text_box = forms.text_box(
			parent=self.rx_ntb.GetPage(0).GetWin(),
			value=self.decim_tb,
			callback=self.set_decim_tb,
			label="Decimation",
			converter=forms.int_converter(),
		)
		self.rx_ntb.GetPage(0).GridAdd(self._decim_tb_text_box, 1, 3, 1, 1)
		self._symb_rate_tb_text_box = forms.text_box(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			value=self.symb_rate_tb,
			callback=self.set_symb_rate_tb,
			label="Symbol rate",
			converter=forms.int_converter(),
		)
		self.rx_ntb.GetPage(1).GridAdd(self._symb_rate_tb_text_box, 2, 1, 1, 1)
		self._satellite_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(0).GetWin(),
			value=self.satellite_text,
			callback=self.set_satellite_text,
			label="Sat ",
			converter=forms.str_converter(),
		)
		self.rx_ntb.GetPage(0).GridAdd(self._satellite_text_static_text, 1, 0, 1, 1)
		self._samp_rate_st_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(0).GetWin(),
			value=self.samp_rate_st,
			callback=self.set_samp_rate_st,
			label="Sample rate",
			converter=forms.float_converter(),
		)
		self.rx_ntb.GetPage(0).GridAdd(self._samp_rate_st_static_text, 1, 4, 1, 1)
		_pll_beta_sl_sizer = wx.BoxSizer(wx.VERTICAL)
		self._pll_beta_sl_text_box = forms.text_box(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			sizer=_pll_beta_sl_sizer,
			value=self.pll_beta_sl,
			callback=self.set_pll_beta_sl,
			label="PLL Beta",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._pll_beta_sl_slider = forms.slider(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			sizer=_pll_beta_sl_sizer,
			value=self.pll_beta_sl,
			callback=self.set_pll_beta_sl,
			minimum=0.000001,
			maximum=0.001,
			num_steps=1000,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.rx_ntb.GetPage(1).GridAdd(_pll_beta_sl_sizer, 2, 0, 1, 1)
		_pll_alpha_sl_sizer = wx.BoxSizer(wx.VERTICAL)
		self._pll_alpha_sl_text_box = forms.text_box(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			sizer=_pll_alpha_sl_sizer,
			value=self.pll_alpha_sl,
			callback=self.set_pll_alpha_sl,
			label="PLL Alpha",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._pll_alpha_sl_slider = forms.slider(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			sizer=_pll_alpha_sl_sizer,
			value=self.pll_alpha_sl,
			callback=self.set_pll_alpha_sl,
			minimum=0.001,
			maximum=0.1,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.rx_ntb.GetPage(1).GridAdd(_pll_alpha_sl_sizer, 1, 0, 1, 1)
		_gain_mu_sl_sizer = wx.BoxSizer(wx.VERTICAL)
		self._gain_mu_sl_text_box = forms.text_box(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			sizer=_gain_mu_sl_sizer,
			value=self.gain_mu_sl,
			callback=self.set_gain_mu_sl,
			label="Gain MU",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._gain_mu_sl_slider = forms.slider(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			sizer=_gain_mu_sl_sizer,
			value=self.gain_mu_sl,
			callback=self.set_gain_mu_sl,
			minimum=0.0001,
			maximum=0.01,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.rx_ntb.GetPage(1).GridAdd(_gain_mu_sl_sizer, 1, 2, 1, 1)
		self._frames_file_text_inf_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(3).GetWin(),
			value=self.frames_file_text_inf,
			callback=self.set_frames_file_text_inf,
			label="Frames filename",
			converter=forms.str_converter(),
		)
		self.rx_ntb.GetPage(3).GridAdd(self._frames_file_text_inf_static_text, 3, 0, 1, 1)
		self._deframer_sync_after_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(2).GetWin(),
			value=self.deframer_sync_after_text,
			callback=self.set_deframer_sync_after_text,
			label="Deframe sync after",
			converter=forms.float_converter(),
		)
		self.rx_ntb.GetPage(2).GridAdd(self._deframer_sync_after_text_static_text, 3, 0, 1, 1)
		self._deframer_nosync_after_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(2).GetWin(),
			value=self.deframer_nosync_after_text,
			callback=self.set_deframer_nosync_after_text,
			label="Deframer out of sync after",
			converter=forms.float_converter(),
		)
		self.rx_ntb.GetPage(2).GridAdd(self._deframer_nosync_after_text_static_text, 4, 0, 1, 1)
		self._deframer_check_sync_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(2).GetWin(),
			value=self.deframer_check_sync_text,
			callback=self.set_deframer_check_sync_text,
			label="Deframer check sync enable",
			converter=forms.str_converter(),
		)
		self.rx_ntb.GetPage(2).GridAdd(self._deframer_check_sync_text_static_text, 2, 0, 1, 1)
		self._datetime_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(3).GetWin(),
			value=self.datetime_text,
			callback=self.set_datetime_text,
			label="Local time of aquisition start",
			converter=forms.str_converter(),
		)
		self.rx_ntb.GetPage(3).GridAdd(self._datetime_text_static_text, 1, 0, 1, 1)
		_clock_alpha_sl_sizer = wx.BoxSizer(wx.VERTICAL)
		self._clock_alpha_sl_text_box = forms.text_box(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			sizer=_clock_alpha_sl_sizer,
			value=self.clock_alpha_sl,
			callback=self.set_clock_alpha_sl,
			label="Clock alpha",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._clock_alpha_sl_slider = forms.slider(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			sizer=_clock_alpha_sl_sizer,
			value=self.clock_alpha_sl,
			callback=self.set_clock_alpha_sl,
			minimum=0.001,
			maximum=0.1,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.rx_ntb.GetPage(1).GridAdd(_clock_alpha_sl_sizer, 1, 1, 1, 1)
		self._baseband_file_text_inf_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(3).GetWin(),
			value=self.baseband_file_text_inf,
			callback=self.set_baseband_file_text_inf,
			label="Baseband filename",
			converter=forms.str_converter(),
		)
		self.rx_ntb.GetPage(3).GridAdd(self._baseband_file_text_inf_static_text, 4, 0, 1, 1)

		##################################################
		# Blocks
		##################################################
		self.cs2cf = gr.interleaved_short_to_complex()
		self.gr_agc_xx_0_0 = gr.agc_cc(10e-6, 1, 1.0/32767.0, 1.0)
		self.gr_binary_slicer_fb_0 = gr.binary_slicer_fb()
		self.gr_clock_recovery_mm_xx_0 = gr.clock_recovery_mm_cc(sps/2.0, clock_alpha**2/4.0, 0.5, gain_mu_sl, max_clock_offset)
		self.gr_complex_to_real_0 = gr.complex_to_real(1)
		self.gr_costas_loop_cc_0 = gr.costas_loop_cc(pll_alpha_sl, pll_beta_sl, 0.07, -0.07, 2)
		self.gr_file_sink_0_0 = gr.file_sink(gr.sizeof_short*1, frames_file)
		self.gr_file_sink_0_0.set_unbuffered(False)
		self.gr_file_source_0 = gr.file_source(gr.sizeof_short*1, baseband_file, False)
		self.gr_moving_average_xx_0 = gr.moving_average_cc(hs, 1.0/hs, 4000)
		self.gr_throttle_0 = gr.throttle(gr.sizeof_short*1, samp_rate*2)
		self.noaa_hrpt_decoder_0 = noaa.hrpt_decoder(True,False)
		self.poesweather_univ_hrpt_deframer_0 = poesweather.univ_hrpt_deframer(deframer_sync_check, 11090, deframer_insync_frames, deframer_outsync_frames)
		self.wxgui_fftsink1 = fftsink2.fft_sink_c(
			self.rx_ntb.GetPage(0).GetWin(),
			baseband_freq=0,
			y_per_div=5,
			y_divs=10,
			ref_level=50,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=30,
			average=True,
			avg_alpha=0.1,
			title="Not filtered spectrum",
			peak_hold=False,
		)
		self.rx_ntb.GetPage(0).Add(self.wxgui_fftsink1.win)
		self.wxgui_scopesink2_1 = scopesink2.scope_sink_c(
			self.rx_ntb.GetPage(1).GetWin(),
			title="PSK constellation diagram",
			sample_rate=symb_rate,
			v_scale=0.4,
			v_offset=0,
			t_scale=1/samp_rate,
			ac_couple=False,
			xy_mode=True,
			num_inputs=1,
			trig_mode=gr.gr_TRIG_MODE_AUTO,
		)
		self.rx_ntb.GetPage(1).Add(self.wxgui_scopesink2_1.win)

		##################################################
		# Connections
		##################################################
		self.connect((self.gr_file_source_0, 0), (self.gr_throttle_0, 0))
		self.connect((self.gr_throttle_0, 0), (self.cs2cf, 0))
		self.connect((self.cs2cf, 0), (self.gr_agc_xx_0_0, 0))
		self.connect((self.cs2cf, 0), (self.wxgui_fftsink1, 0))
		self.connect((self.gr_complex_to_real_0, 0), (self.gr_binary_slicer_fb_0, 0))
		self.connect((self.poesweather_univ_hrpt_deframer_0, 0), (self.gr_file_sink_0_0, 0))
		self.connect((self.gr_binary_slicer_fb_0, 0), (self.poesweather_univ_hrpt_deframer_0, 0))
		self.connect((self.poesweather_univ_hrpt_deframer_0, 0), (self.noaa_hrpt_decoder_0, 0))
		self.connect((self.gr_moving_average_xx_0, 0), (self.gr_clock_recovery_mm_xx_0, 0))
		self.connect((self.gr_agc_xx_0_0, 0), (self.gr_costas_loop_cc_0, 0))
		self.connect((self.gr_costas_loop_cc_0, 0), (self.gr_moving_average_xx_0, 0))
		self.connect((self.gr_clock_recovery_mm_xx_0, 0), (self.gr_complex_to_real_0, 0))
		self.connect((self.gr_clock_recovery_mm_xx_0, 0), (self.wxgui_scopesink2_1, 0))

	def set_satellite(self, satellite):
		self.satellite = satellite
		self.set_satellite_text(self.satellite)

	def set_decim(self, decim):
		self.decim = decim
		self.set_decim_tb(self.decim)

	def set_baseband_file(self, baseband_file):
		self.baseband_file = baseband_file
		self.set_baseband_file_text_inf(self.baseband_file)

	def set_frames_file(self, frames_file):
		self.frames_file = frames_file
		self.set_frames_file_text_inf(self.frames_file)

	def set_deframer_outsync_frames(self, deframer_outsync_frames):
		self.deframer_outsync_frames = deframer_outsync_frames
		self.set_deframer_nosync_after_text(self.deframer_outsync_frames)

	def set_deframer_insync_frames(self, deframer_insync_frames):
		self.deframer_insync_frames = deframer_insync_frames
		self.set_deframer_sync_after_text(self.deframer_insync_frames)

	def set_clock_alpha(self, clock_alpha):
		self.clock_alpha = clock_alpha
		self.set_clock_alpha_sl(self.clock_alpha)
		self.gr_clock_recovery_mm_xx_0.set_gain_omega(self.clock_alpha**2/4.0)

	def set_gain_mu(self, gain_mu):
		self.gain_mu = gain_mu
		self.set_gain_mu_sl(self.gain_mu)

	def set_pll_alpha(self, pll_alpha):
		self.pll_alpha = pll_alpha
		self.set_pll_alpha_sl(self.pll_alpha)

	def set_pll_beta(self, pll_beta):
		self.pll_beta = pll_beta
		self.set_pll_beta_sl(self.pll_beta)

	def set_deframer_sync_check(self, deframer_sync_check):
		self.deframer_sync_check = deframer_sync_check
		self.set_deframer_check_sync_text(self.deframer_sync_check)

	def set_symb_rate(self, symb_rate):
		self.symb_rate = symb_rate
		self.set_symb_rate_tb(self.symb_rate)
		self.wxgui_scopesink2_1.set_sample_rate(self.symb_rate)

	def set_decim_tb(self, decim_tb):
		self.decim_tb = decim_tb
		self.set_samp_rate(100e6/self.decim_tb)
		self._decim_tb_text_box.set_value(self.decim_tb)

	def set_symb_rate_tb(self, symb_rate_tb):
		self.symb_rate_tb = symb_rate_tb
		self.set_sps(self.samp_rate/self.symb_rate_tb)
		self._symb_rate_tb_text_box.set_value(self.symb_rate_tb)

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.set_samp_rate_st(self.samp_rate)
		self.set_sps(self.samp_rate/self.symb_rate_tb)
		self.wxgui_fftsink1.set_sample_rate(self.samp_rate)
		self.set_max_carrier_offset(2*math.pi*100e3/self.samp_rate)

	def set_sps(self, sps):
		self.sps = sps
		self.set_hs(int(self.sps/2.0))
		self.gr_clock_recovery_mm_xx_0.set_omega(self.sps/2.0)

	def set_satellite_text(self, satellite_text):
		self.satellite_text = satellite_text
		self._satellite_text_static_text.set_value(self.satellite_text)

	def set_samp_rate_st(self, samp_rate_st):
		self.samp_rate_st = samp_rate_st
		self._samp_rate_st_static_text.set_value(self.samp_rate_st)

	def set_pll_beta_sl(self, pll_beta_sl):
		self.pll_beta_sl = pll_beta_sl
		self._pll_beta_sl_slider.set_value(self.pll_beta_sl)
		self._pll_beta_sl_text_box.set_value(self.pll_beta_sl)
		self.gr_costas_loop_cc_0.set_beta(self.pll_beta_sl)

	def set_pll_alpha_sl(self, pll_alpha_sl):
		self.pll_alpha_sl = pll_alpha_sl
		self._pll_alpha_sl_slider.set_value(self.pll_alpha_sl)
		self._pll_alpha_sl_text_box.set_value(self.pll_alpha_sl)
		self.gr_costas_loop_cc_0.set_alpha(self.pll_alpha_sl)

	def set_max_clock_offset(self, max_clock_offset):
		self.max_clock_offset = max_clock_offset

	def set_max_carrier_offset(self, max_carrier_offset):
		self.max_carrier_offset = max_carrier_offset

	def set_hs(self, hs):
		self.hs = hs
		self.gr_moving_average_xx_0.set_length_and_scale(self.hs, 1.0/self.hs)

	def set_gain_mu_sl(self, gain_mu_sl):
		self.gain_mu_sl = gain_mu_sl
		self.gr_clock_recovery_mm_xx_0.set_gain_mu(self.gain_mu_sl)
		self._gain_mu_sl_slider.set_value(self.gain_mu_sl)
		self._gain_mu_sl_text_box.set_value(self.gain_mu_sl)

	def set_frames_file_text_inf(self, frames_file_text_inf):
		self.frames_file_text_inf = frames_file_text_inf
		self._frames_file_text_inf_static_text.set_value(self.frames_file_text_inf)

	def set_deframer_sync_after_text(self, deframer_sync_after_text):
		self.deframer_sync_after_text = deframer_sync_after_text
		self._deframer_sync_after_text_static_text.set_value(self.deframer_sync_after_text)

	def set_deframer_nosync_after_text(self, deframer_nosync_after_text):
		self.deframer_nosync_after_text = deframer_nosync_after_text
		self._deframer_nosync_after_text_static_text.set_value(self.deframer_nosync_after_text)

	def set_deframer_check_sync_text(self, deframer_check_sync_text):
		self.deframer_check_sync_text = deframer_check_sync_text
		self._deframer_check_sync_text_static_text.set_value(self.deframer_check_sync_text)

	def set_datetime_text(self, datetime_text):
		self.datetime_text = datetime_text
		self._datetime_text_static_text.set_value(self.datetime_text)

	def set_clock_alpha_sl(self, clock_alpha_sl):
		self.clock_alpha_sl = clock_alpha_sl
		self._clock_alpha_sl_slider.set_value(self.clock_alpha_sl)
		self._clock_alpha_sl_text_box.set_value(self.clock_alpha_sl)

	def set_baseband_file_text_inf(self, baseband_file_text_inf):
		self.baseband_file_text_inf = baseband_file_text_inf
		self._baseband_file_text_inf_static_text.set_value(self.baseband_file_text_inf)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	parser.add_option("", "--satellite", dest="satellite", type="string", default='NOAAxx',
		help="Set Satellite [default=%default]")
	parser.add_option("", "--decim", dest="decim", type="intx", default=50,
		help="Set Decimation [default=%default]")
	parser.add_option("", "--baseband-file", dest="baseband_file", type="string", default="/home/martin/GNURadioData/hrpt/baseband/HRPT_NOAA19_2010-09-10_12-35-34_UTC_U2_d50.sam",
		help="Set Baseband output filename [default=%default]")
	parser.add_option("", "--frames-file", dest="frames_file", type="string", default=os.environ['HOME'] + '/noaa_hrpt_frames.hmf',
		help="Set hmf output filename [default=%default]")
	parser.add_option("", "--deframer-outsync-frames", dest="deframer_outsync_frames", type="intx", default=5,
		help="Set Count of invalid ASM's after which deframer go out of synced state [default=%default]")
	parser.add_option("", "--deframer-insync-frames", dest="deframer_insync_frames", type="intx", default=2,
		help="Set Count of valid ASM's after which deframer go in to synced state [default=%default]")
	parser.add_option("", "--clock-alpha", dest="clock_alpha", type="eng_float", default=eng_notation.num_to_str(0.005),
		help="Set Clock alpha [default=%default]")
	parser.add_option("", "--gain-mu", dest="gain_mu", type="eng_float", default=eng_notation.num_to_str(0.005),
		help="Set Gain MU [default=%default]")
	parser.add_option("", "--pll-alpha", dest="pll_alpha", type="eng_float", default=eng_notation.num_to_str(0.005),
		help="Set PLL alpha [default=%default]")
	parser.add_option("", "--pll-beta", dest="pll_beta", type="eng_float", default=eng_notation.num_to_str(0.00001),
		help="Set PLL beta [default=%default]")
	parser.add_option("", "--deframer-sync-check", dest="deframer_sync_check", type="intx", default=True,
		help="Set Deframer synchronisation check active [default=%default]")
	parser.add_option("", "--symb-rate", dest="symb_rate", type="eng_float", default=eng_notation.num_to_str(600*1109),
		help="Set Symbol rate [default=%default]")
	(options, args) = parser.parse_args()
	tb = bb_rx_noaa_hrpt_fr_ver2(satellite=options.satellite, decim=options.decim, baseband_file=options.baseband_file, frames_file=options.frames_file, deframer_outsync_frames=options.deframer_outsync_frames, deframer_insync_frames=options.deframer_insync_frames, clock_alpha=options.clock_alpha, gain_mu=options.gain_mu, pll_alpha=options.pll_alpha, pll_beta=options.pll_beta, deframer_sync_check=options.deframer_sync_check, symb_rate=options.symb_rate)
	tb.Run(True)

