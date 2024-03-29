#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
区块拟合尝试与验证
@author: zhengxiaoyao0716
"""

import random
import math
from matplotlib import pyplot as plt, figure, axes

from init_plot import run
from sphere import draw_sphere, Samples

range = xrange


def projection(xs, ys, zs):
    """三维坐标到二维投影"""
    def rotate(us, vs):
        """二维坐标旋转"""
        u, v = us[0], vs[0]  # 法向量
        l = math.sqrt(math.pow(u, 2) + math.pow(v, 2))  # 长度
        cosa, sina = u / l, -v / l  # 旋转角
        ru, rv = [], []
        for u, v in ((us[i], vs[i]) for i in range(len(us))):
            ru.append(u * cosa - v * sina)
            rv.append(u * sina + v * cosa)
        return ru, rv
    zs, xs = rotate(zs, xs)
    zs, ys = rotate(zs, ys)
    return xs, ys


def main(fig):
    """
    Entrypoint
    :type fig: figure.Figure
    """
    # 建模采样
    samples = Samples(300)
    point = samples.point(random.randint(0, samples.n - 1))
    area = samples.area(point)
    xyzs = zip(point.coord, *area)

    # 准备绘制
    gs = plt.GridSpec(2, 2, width_ratios=[2, 5])

    ax_view = fig.add_subplot(gs[0], projection='3d')  # type: axes.Axes
    ax_view.set_title(u'球面鸟瞰')

    ax_focus = fig.add_subplot(gs[2], projection='3d')  # type: axes.Axes
    ax_focus.set_title(u'区块聚焦')

    ax = fig.add_subplot(gs[1:4:2])  # type: axes.Axes
    ax.set_title(u'区块拟合')

    for ax in [ax_view, ax_focus, ax]:
        ax.set_aspect('equal', adjustable='datalim')

    # 绘制球体
    draw_sphere(ax_view, 0.1)

    # 绘制样点
    color = [
        '#000000',  # 中心样本点
        '#ff0000', '#ff9900', '#ffff00', '#00ff00',
        '#00ffff', '#0000ff', '#9900ff', '#ff00ff'
    ][:len(xyzs[0])]
    ax_view.scatter(*xyzs, c=color)
    ax_focus.scatter(*xyzs, c=color)
    ax.scatter(*projection(*xyzs), c=color)


if __name__ == '__main__':
    run(main)
